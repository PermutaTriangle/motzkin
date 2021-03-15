from itertools import chain
from typing import Iterator, Optional, Tuple, cast

from comb_spec_searcher import (
    AtomStrategy,
    CartesianProductStrategy,
    DisjointUnionStrategy,
    StrategyFactory,
    StrategyPack,
)

from motzkinpaths import (
    CrossingPattern,
    MotzkinPaths,
    MotzkinPathsStartingWithH,
    MotzkinPathsStartingWithU,
)
from motzkinpatterns import MotzkinPath


class Expansion(DisjointUnionStrategy):
    def decomposition_function(
        self, motzkin_paths: MotzkinPaths
    ) -> Optional[Tuple[MotzkinPaths, ...]]:
        if isinstance(motzkin_paths, MotzkinPathsStartingWithH) or isinstance(
            motzkin_paths, MotzkinPathsStartingWithU
        ):
            return None
        empty = MotzkinPaths(("UD", "H"), motzkin_paths.contains)
        avh = MotzkinPathsStartingWithH(motzkin_paths.avoids, motzkin_paths.contains)
        avu = MotzkinPathsStartingWithU(motzkin_paths.avoids, motzkin_paths.contains)
        return (empty, avh, avu)

    def formal_step(self) -> str:
        return "A path is empty, starts with H, or starts with U"

    @classmethod
    def from_dict(cls, d: dict) -> "Expansion":
        return Expansion(
            ignore_parent=d.pop("ignore_parent"),
            inferrable=d.pop("inferrable"),
            possibly_empty=d.pop("possibly_empty"),
            workable=d.pop("workable"),
        )

    def forward_map(
        self,
        motzkin_paths: MotzkinPaths,
        path: MotzkinPath,
        children: Optional[Tuple[MotzkinPaths, ...]] = None,
    ) -> Tuple[Optional[MotzkinPath], ...]:
        if path.is_empty():
            return (path, None, None)
        if path[0] == "H":
            return (None, path, None)
        return (None, None, path)


class PattInsertion(DisjointUnionStrategy):
    def __init__(
        self,
        pattern: MotzkinPath,
        ignore_parent=False,
        inferrable=True,
        possibly_empty=True,
        workable=True,
    ):
        self.pattern = pattern
        super().__init__(
            ignore_parent=ignore_parent,
            inferrable=inferrable,
            possibly_empty=possibly_empty,
            workable=workable,
        )

    def decomposition_function(
        self, motzkin_paths: MotzkinPaths
    ) -> Tuple[MotzkinPaths, ...]:
        return (
            motzkin_paths.add_avoid(self.pattern),
            motzkin_paths.add_contain(self.pattern),
        )

    def formal_step(self) -> str:
        return f"The paths avoid or contain {self.pattern}"

    @classmethod
    def from_dict(cls, d: dict) -> "PattInsertion":
        return PattInsertion(
            pattern=MotzkinPath.from_dict(d.pop("pattern")),
            ignore_parent=d.pop("ignore_parent"),
            inferrable=d.pop("inferrable"),
            possibly_empty=d.pop("possibly_empty"),
            workable=d.pop("workable"),
        )

    def forward_map(
        self,
        motzkin_paths: MotzkinPaths,
        path: MotzkinPath,
        children: Optional[Tuple[MotzkinPaths, ...]] = None,
    ) -> Tuple[Optional[MotzkinPath], ...]:
        if path.avoids(self.pattern):
            return (path, None)
        return (None, path)


class PattInsertionFactory(StrategyFactory):
    def __call__(
        self, motzkin_paths: MotzkinPaths, **kwargs
    ) -> Iterator[PattInsertion]:
        if isinstance(motzkin_paths, MotzkinPathsStartingWithU):
            for cp in chain(motzkin_paths.avoids, *motzkin_paths.contains):
                if not cp.is_localised():
                    cpleft = CrossingPattern(cp.left, "")
                    cpright = CrossingPattern("", cp.right)
                    yield PattInsertion(cpleft)
                    yield PattInsertion(cpright)
        for cp in chain(
            *[p_list for p_list in motzkin_paths.contains if len(p_list) > 1]
        ):
            yield PattInsertion(cp)

    @classmethod
    def from_dict(cls, d: dict) -> "PattInsertionFactory":
        return PattInsertionFactory()

    def __repr__(self) -> str:
        return "PatternInsertionFactory()"

    def __str__(self) -> str:
        return "pattern insertions"


class Factor(CartesianProductStrategy):
    def decomposition_function(
        self, motzkin_paths: MotzkinPaths
    ) -> Optional[Tuple[MotzkinPaths, ...]]:
        if isinstance(motzkin_paths, MotzkinPathsStartingWithH) or isinstance(
            motzkin_paths, MotzkinPathsStartingWithU
        ):
            return motzkin_paths.factors()
        return None

    def formal_step(self) -> str:
        return "Remove known letters."

    @classmethod
    def from_dict(cls, d: dict) -> "Factor":
        return Factor(
            ignore_parent=d.pop("ignore_parent"),
            inferrable=d.pop("inferrable"),
            possibly_empty=d.pop("possibly_empty"),
            workable=d.pop("workable"),
        )

    def backward_map(
        self,
        motzkin_paths: MotzkinPaths,
        objs: Tuple[Optional[MotzkinPath], ...],
        children: Optional[Tuple[MotzkinPaths, ...]] = None,
    ) -> Iterator[MotzkinPath]:
        if isinstance(motzkin_paths, MotzkinPathsStartingWithU):
            assert isinstance(objs[1], MotzkinPath)
            yield MotzkinPath(("U",) + objs[1] + ("D",) + objs[2])
        elif isinstance(motzkin_paths, MotzkinPathsStartingWithH):
            assert isinstance(objs[1], MotzkinPath)
            yield MotzkinPath(("H",) + objs[1])

    def forward_map(
        self,
        motzkin_paths: MotzkinPaths,
        path: MotzkinPath,
        children: Optional[Tuple[MotzkinPaths, ...]] = None,
    ) -> Tuple[Optional[MotzkinPath], ...]:
        raise NotImplementedError


pack = StrategyPack(
    initial_strats=[Factor()],
    inferral_strats=[],
    expansion_strats=[[Expansion(), PattInsertionFactory()]],
    ver_strats=[AtomStrategy()],
    name=("Finding specification for words avoiding patterns."),
)

if __name__ == "__main__":
    strat = Expansion()
    print(repr(strat))
    print(
        Expansion(
            ignore_parent=False, inferrable=True, possibly_empty=True, workable=True
        )
    )

    assert strat == DisjointUnionStrategy.from_dict(strat.to_jsonable())

    strat2 = PattInsertionFactory()
    print(strat2)
    print(repr(strat2))

    assert strat2 == StrategyFactory.from_dict(strat2.to_jsonable())

    strat3 = Factor()
    assert strat3 == CartesianProductStrategy.from_dict(strat3.to_jsonable())

    print(pack)

    from comb_spec_searcher import CombinatorialSpecificationSearcher
    from comb_spec_searcher.utils import maple_equations

    patts = [MotzkinPath("UHD", True), MotzkinPath("DHU", True)]
    start_class = MotzkinPaths(patts)
    searcher = CombinatorialSpecificationSearcher(start_class, pack, debug=False)

    spec = searcher.auto_search(status_update=10)
    print(spec)
    spec.show()
    f = spec.get_genf()

    print(f)

    print(spec.random_sample_object_of_size(15))
    for i in range(100):
        print(f"=== {i} ===")
        print(spec.count_objects_of_size(i))
        assert start_class.get_terms(i) == spec.get_terms(i)
