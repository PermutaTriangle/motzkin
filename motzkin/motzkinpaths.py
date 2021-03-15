"""
This module contains classes for generating all motzkin paths avoiding and
containing some patterns. There are three classes: all, starting with H,
starting with U. The latter is done in more generality in terms of crossing
patterns.

They are all instances of CombinatorialClass, and used for
performing combinatorial exploration on pattern avoiding Motzkin paths.
"""
from itertools import chain
from typing import Iterable, Iterator, List, Optional, Set, Tuple, Union

import sympy
from comb_spec_searcher import CombinatorialClass

from motzkinpatterns import CrossingPattern, MotzkinPath

__all__ = ["MotzkinPaths", "MotzkinPathsStartingWithH", "MotzkinPathsStartingWithU"]


class MotzkinPaths(CombinatorialClass):
    def __init__(
        self,
        avoids: Iterable[Iterable[str]] = tuple(),
        contains: Iterable[Iterable[Iterable[str]]] = tuple(),
    ):
        if any(isinstance(p, str) for p in avoids):
            avoids = tuple(MotzkinPath(p, True) for p in avoids)
        if any(isinstance(p, str) for p in chain(*[p_list for p_list in contains])):
            contains = tuple(
                tuple(MotzkinPath(p, True) for p in p_list) for p_list in contains
            )
        if self.__class__ == MotzkinPath:
            for patt in chain(avoids, *contains):
                if not all(l in ("U", "D", "H") for l in patt):
                    raise ValueError('All letters must be "U", "D", or "H"')
        self.avoids: Tuple[MotzkinPath, ...] = tuple(sorted(set(avoids)))
        self.contains: Tuple[MotzkinPath, ...] = tuple(
            sorted(tuple(sorted(set(p_list))) for p_list in contains)
        )
        self._cleanup()
        self._motzkinify()
        self._cleanup()

    def _motzkinify(self) -> None:
        self.avoids = tuple(
            sorted(
                p
                for p in chain(
                    *[patt.minimal_set_for_avoidance() for patt in self.avoids]
                )
            )
        )
        self.contains = tuple(
            sorted(
                tuple(
                    sorted(
                        p
                        for p in chain(
                            *[patt.minimal_set_for_avoidance() for patt in p_list]
                        )
                    )
                )
                for p_list in self.contains
            )
        )

    def _cleanup(self) -> None:
        while True:
            minav = self._minimised_avoids()
            minav, minco = self._minimised_contains(minav)
            if self.avoids == minav and self.contains == minco:
                break
            else:
                self.avoids = minav
                self.contains = minco

    def _minimised_avoids(
        self, avoids: Optional[Tuple[Union[CrossingPattern, MotzkinPath], ...]] = None
    ) -> Tuple[Union[CrossingPattern, MotzkinPath], ...]:
        """Reduces the patterns to be avoided with respect to
        containment."""
        if avoids is None:
            avoids = self.avoids
        cleaned_av: List[MotzkinPath] = []
        for av in avoids:
            if all(p not in av for p in cleaned_av):
                cleaned_av.append(av)
        return tuple(sorted(cleaned_av))

    def _minimised_contains(
        self,
        minimized_avoids: Tuple[Union[CrossingPattern, MotzkinPath], ...],
        contains: Optional[
            Tuple[Tuple[Union[CrossingPattern, MotzkinPath], ...], ...]
        ] = None,
    ) -> Tuple[
        Tuple[Union[CrossingPattern, MotzkinPath], ...],
        Tuple[Tuple[Union[CrossingPattern, MotzkinPath], ...], ...],
    ]:
        """First removes all patterns from container lists if the
        contain something which must be avoided. Then removes all container
        lists which are implied by other lists."""
        # remove any redundant patterns from each list of patterns
        # this is just the minimal set
        if contains is None:
            contains = self.contains
        cleaned_cos: List[List[MotzkinPath]] = []
        for co in chain([self.__class__.class_req()], contains):
            if not all(co):
                continue
            redundant: Set[int] = set()
            for i, c1 in enumerate(co):
                for j, c2 in enumerate(co[i + 1 :]):
                    k = j + i + 1
                    if k not in redundant:
                        if c1 in c2:
                            redundant.add(k)
                if i not in redundant:
                    if any(p in c1 for p in minimized_avoids):
                        redundant.add(i)
            clean_co = [p for i, p in enumerate(co) if i not in redundant]
            if not clean_co:
                # if becomes empty then can not contain so set is empty.
                return self.__class__.obs_reqs_for_empty()
            cleaned_cos.append(clean_co)

        # remove lists that are implied by other lists
        redundant = set()
        for i, cos in enumerate(cleaned_cos):
            if i not in redundant:
                for j, cos2 in enumerate(cleaned_cos):
                    if i != j and j not in redundant:
                        if all(any(p2 in p1 for p2 in cos2) for p1 in cos):
                            redundant.add(j)
        cleaned_cos = [co for i, co in enumerate(cleaned_cos) if i not in redundant]
        return minimized_avoids, tuple(sorted(tuple(sorted(co)) for co in cleaned_cos))

    def add_avoid(self, patt: MotzkinPath) -> "MotzkinPaths":
        return self.__class__(avoids=self.avoids + (patt,), contains=self.contains)

    def add_contain(self, patt: MotzkinPath) -> "MotzkinPaths":
        return self.__class__(avoids=self.avoids, contains=self.contains + ((patt,),))

    @classmethod
    def class_req(cls) -> Tuple[MotzkinPath]:
        return (MotzkinPath(),)

    @classmethod
    def obs_reqs_for_empty(cls) -> Tuple[Tuple[MotzkinPath], Tuple]:
        return (MotzkinPath(),), tuple()

    def is_empty(self) -> bool:
        if (self.avoids, self.contains) == self.__class__.obs_reqs_for_empty():
            return True
        iterator = chain(*[self.objects_of_size(i) for i in range(self.maxlen() + 1)])
        try:
            next(iterator)
            return False
        except StopIteration:
            # if not (self.avoids, self.contains) == self.__class__.obs_reqs_for_empty():
            #     print(self, self.maxlen())
            #     input()
            return True

    def maxlen(self) -> int:
        return sum(max(len(p) for p in p_list) for p_list in self.contains)

    @classmethod
    def justH(cls) -> "MotzkinPaths":
        return MotzkinPaths(avoids=["UD", "HH"], contains=["H"])

    @classmethod
    def justUD(cls) -> "MotzkinPaths":
        return MotzkinPaths(avoids=["H", "UDUD", "UUDD"], contains=[["UD"]])

    @classmethod
    def justempty(cls) -> "MotzkinPaths":
        return MotzkinPaths(avoids=["UD", "H"])

    def is_epsilon(self) -> bool:
        return self == MotzkinPaths.justempty()

    def is_atom(self) -> bool:
        return self in (self.justempty(), self.justH(), self.justUD())

    def minimum_size_of_object(self) -> int:
        if not self.contains:
            return 0
        return max(min(len(p) for p in patts) for patts in self.contains)

    def is_positive(self) -> bool:
        return bool(self.contains)

    def objects_of_size(self, size: int) -> Iterator[MotzkinPath]:
        def all_motzkin_paths(size):
            if size < 0:
                return
            if size == 0:
                yield MotzkinPath()
                return
            if size == 1:
                yield MotzkinPath("H")
                return
            for path in all_motzkin_paths(size - 1):
                yield MotzkinPath(("H",) + path)
            for i in range(size - 1):
                for p1 in all_motzkin_paths(i):
                    for p2 in all_motzkin_paths(size - i - 2):
                        yield MotzkinPath(("U",) + p1 + ("D",) + p2)

        for p in all_motzkin_paths(size):
            if all(p.avoids(patt) for patt in self.avoids) and all(
                any(p.contains(patt) for patt in co_list) for co_list in self.contains
            ):
                yield p

    def to_jsonable(self, prefix="") -> dict:
        return {"prefix": prefix, "avoids": self.avoids, "contains": self.contains}

    @classmethod
    def from_dict(cls, d: dict) -> "MotzkinPaths":
        prefix = d.pop("prefix")
        avoids_json = d.pop("avoids")
        contains_json = d.pop("contains")
        if prefix == "U":
            crossing_avoids = tuple(
                CrossingPattern.from_dict(patt) for patt in avoids_json
            )
            crossing_contains = tuple(
                tuple(CrossingPattern.from_dict(patt) for patt in pattlist)
                for pattlist in contains_json
            )
            return MotzkinPathsStartingWithU(
                crossing_avoids=crossing_avoids, crossing_contains=crossing_contains
            )
        avoids = tuple(MotzkinPath.from_dict(patt) for patt in avoids_json)
        contains = tuple(
            tuple(MotzkinPath.from_dict(patt) for patt in pattlist)
            for pattlist in contains_json
        )
        if prefix == "H":
            return MotzkinPathsStartingWithH(avoids, contains)
        return MotzkinPaths(avoids, contains)

    def __eq__(self, other) -> bool:
        if isinstance(other, MotzkinPaths):
            return (
                type(self) == type(other)
                and self.avoids == other.avoids
                and self.contains == other.contains
            )
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(hash(self.avoids) + hash(self.contains))

    def __repr__(self) -> str:
        return "MotzkinPaths({}, {})".format(repr(self.avoids), repr(self.contains))

    def __str__(self, extra: str = "") -> str:
        if self == self.justH():
            return "{H}"
        if self == self.justUD():
            return "{UD}"
        if self == self.justempty():
            return "{\u03BB}"
        if self.is_empty():
            return "\u2205"

        avoids = ", ".join(str(p) for p in self.avoids)
        contains = "".join(
            "\u2229Co({})".format(", ".join(str(p) for p in p_list))
            for p_list in self.contains
        )
        return "Av{}({}){}".format(extra, avoids, contains)


class MotzkinPathsStartingWithH(MotzkinPaths):
    def __init__(
        self,
        avoids: Iterable[MotzkinPath] = tuple(),
        contains: Iterable[Iterable[MotzkinPath]] = tuple(),
    ):
        if MotzkinPath("H") not in contains:
            contains = tuple(contains) + (MotzkinPath("H"),)
        if self.__class__ == MotzkinPathsStartingWithH:
            for patt in chain(avoids, *contains):
                if not all(l in ("U", "D", "H") for l in patt):
                    raise ValueError('All letters must be "U", "D", or "H"')
        MotzkinPaths.__init__(self, avoids, contains)

    def factors(self) -> List[MotzkinPaths]:
        """Return the factors obtained by removing the H from the front."""

        def stripH(patt):
            if len(patt) > 0 and patt[0] == "H":
                return MotzkinPath(patt[1:], pattern=True)
            return MotzkinPath(patt, pattern=True)

        h = MotzkinPaths.justH()
        rest = MotzkinPaths(
            avoids=[stripH(p) for p in self.avoids],
            contains=[[stripH(p) for p in p_list] for p_list in self.contains],
        )
        return [h, rest]

    def from_parts(self, *args, **kwargs) -> MotzkinPath:
        _, rest = self.factors()
        rest_obj = None
        for obj, comb_class in args:
            if comb_class == rest:
                rest_obj = obj
                break
        assert rest_obj is not None
        return MotzkinPath(("H",) + rest_obj)

    @classmethod
    def class_req(cls) -> Tuple[MotzkinPath]:
        return (MotzkinPath("H"),)

    @classmethod
    def obs_reqs_for_empty(cls) -> Tuple[Tuple[MotzkinPath], Tuple]:
        return (MotzkinPath(),), tuple()

    def objects_of_size(self, size: int) -> Iterator[MotzkinPath]:
        if size <= 0:
            return
        for path in MotzkinPaths.objects_of_size(self, size):
            if path[0] == "H":
                yield path

    def maxlen(self) -> int:
        return MotzkinPaths.maxlen(self) + (
            0
            if all(all(p[0] == "H" for p in p_list) for p_list in self.contains)
            else 1
        )

    def to_jsonable(self, prefix: str = "H") -> dict:
        return MotzkinPaths.to_jsonable(self, prefix=prefix)

    def is_empty(self) -> bool:
        if MotzkinPath("H") in self.avoids:
            return True
        else:
            return MotzkinPaths.is_empty(self)

    def __repr__(self) -> str:
        return "MotzkinPathsStartingWithH({}, {})".format(
            repr(self.avoids), repr(self.contains)
        )

    def __str__(self, extra: str = "") -> str:
        return MotzkinPaths.__str__(self, extra="H")


class MotzkinPathsStartingWithU(MotzkinPaths):
    def __init__(
        self,
        avoids: Optional[Iterable[MotzkinPath]] = None,
        contains: Optional[Iterable[Iterable[MotzkinPath]]] = None,
        crossing_avoids: Optional[Iterable[MotzkinPath]] = None,
        crossing_contains: Optional[Iterable[Iterable[CrossingPattern]]] = None,
    ):
        if avoids is not None or contains is not None:
            if crossing_avoids is not None or crossing_contains is not None:
                raise ValueError(
                    (
                        "Either initialise with crossing patterns "
                        "or patterns, not with both."
                    )
                )
            if avoids is None:
                avoids = tuple()
            if contains is None:
                contains = tuple()
            crossing_avoids = []
            crossing_contains = []
            for patt in avoids:
                cps = CrossingPattern.all_crossing_patterns(patt)
                crossing_avoids.extend(cps)
            for patt_list in contains:
                cp_list = []
                for patt in patt_list:
                    cps = CrossingPattern.all_crossing_patterns(patt)
                    cp_list.extend(cps)
                crossing_contains.append(tuple(cp_list))
        else:
            if crossing_avoids is None:
                crossing_avoids = tuple()
            if crossing_contains is None:
                crossing_contains = tuple()
            for crossing_patt in chain(crossing_avoids, *crossing_contains):
                if not isinstance(crossing_patt, CrossingPattern):
                    raise TypeError(
                        (
                            "Patterns passed in for crossing must be"
                            "of type CrossingPattern."
                        )
                    )
        MotzkinPaths.__init__(self, crossing_avoids, crossing_contains)

    def factors(self) -> Optional[Tuple[MotzkinPaths, MotzkinPaths, MotzkinPaths]]:
        """Return list of factors if all crossing patterns are localised."""

        def stripUD(patt):
            mindex = 0
            maxdex = len(patt)
            if len(patt) > 0:
                if patt[0] == "U":
                    mindex += 1
                if patt[-1] == "D":
                    maxdex -= 1
            return MotzkinPath(patt[mindex:maxdex], pattern=True)

        if all(p.is_localised() for p in self.avoids) and all(
            len(p_list) == 1 and p_list[0].is_localised() for p_list in self.contains
        ):
            ud = MotzkinPaths.justUD()
            avleft, coleft, avright, coright = [], [], [], []
            for p in self.avoids:
                if p.is_left_localised():
                    avleft.append(stripUD(p.left))
                else:
                    avright.append(p.right)
            for p_list in self.contains:
                p = p_list[0]
                if p.is_left_localised():
                    coleft.append((stripUD(p.left),))
                else:
                    coright.append((p.right,))
            left = MotzkinPaths(avleft, coleft)
            right = MotzkinPaths(avright, coright)
            return (ud, left, right)
        return None

    def from_parts(self, *args, **kwargs) -> MotzkinPath:
        factors = self.factors()
        assert factors is not None
        _, left, right = factors
        left_obj, right_obj = None, None
        for obj, comb_class in args:
            if comb_class == left:
                left_obj = obj
            elif comb_class == right:
                right_obj = obj
        assert left_obj is not None and right_obj is not None
        return MotzkinPath(("U",) + left_obj + ("D",) + right_obj)

    @classmethod
    def class_req(cls) -> Tuple[CrossingPattern]:
        return (CrossingPattern("UD", ""),)

    @classmethod
    def obs_reqs_for_empty(cls) -> Tuple[Tuple[CrossingPattern], Tuple]:
        return (CrossingPattern("", ""),), tuple()

    def maxlen(self) -> int:
        return MotzkinPaths.maxlen(self) + 2

    def _minimised_avoids(
        self, avoids: Optional[Tuple[Union[CrossingPattern, MotzkinPath], ...]] = None
    ) -> Tuple[Union[CrossingPattern, MotzkinPath], ...]:
        if avoids is None:
            avoids = self.avoids
        new_av = list(self.avoids)
        for co in self.contains:
            if len(co) == 1:
                co = co[0]
                if co.is_left_localised():
                    for av in self.avoids:
                        if not av.is_left_localised() and av.left == co.left:
                            new_av.append(CrossingPattern([], av.right))
                if co.is_right_localised():
                    for av in self.avoids:
                        if not av.is_right_localised() and av.right == co.right:
                            new_av.append(CrossingPattern(av.left, []))
        avoids = tuple(sorted(new_av))
        return MotzkinPaths._minimised_avoids(self, avoids=avoids)

    def _minimised_contains(
        self,
        minimized_avoids: Tuple[Union[CrossingPattern, MotzkinPath], ...],
        contains: Optional[
            Tuple[Tuple[Union[CrossingPattern, MotzkinPath], ...], ...]
        ] = None,
    ) -> Tuple[
        Tuple[Union[CrossingPattern, MotzkinPath], ...],
        Tuple[Tuple[Union[CrossingPattern, MotzkinPath], ...], ...],
    ]:
        """First removes all patterns from container lists if the
        contain something which must be avoided. Then removes all container
        lists which are implied by other lists."""
        if contains is None:
            new_contains = set()
            for cp_list in self.contains:
                if len(cp_list) == 1 and not cp_list[0].is_localised():
                    cp = cp_list[0]
                    new_contains.add((CrossingPattern(cp.left, ""),))
                    new_contains.add((CrossingPattern("", cp.right),))
                else:
                    new_contains.add(cp_list)
            contains = tuple(
                sorted(tuple(sorted(co for co in co_list)) for co_list in new_contains)
            )
        return MotzkinPaths._minimised_contains(self, minimized_avoids, contains)

    def add_avoid(self, patt: CrossingPattern) -> "MotzkinPathsStartingWithU":
        return MotzkinPathsStartingWithU(
            crossing_avoids=self.avoids + (patt,), crossing_contains=self.contains
        )

    def add_contain(self, patt: CrossingPattern) -> "MotzkinPathsStartingWithU":
        return MotzkinPathsStartingWithU(
            crossing_avoids=self.avoids, crossing_contains=self.contains + ((patt,),)
        )

    def objects_of_size(self, size: int) -> Iterator[MotzkinPath]:
        if size <= 0:
            return
        for path in MotzkinPaths.objects_of_size(self, size):
            if path[0] == "U":
                yield path

    def to_jsonable(self, prefix="U") -> dict:
        return {
            "prefix": prefix,
            "crossing_avoids": tuple(p.to_jsonable() for p in self.avoids),
            "crossing_contains": tuple(
                p.to_jsonable() for ps in self.contains for p in ps
            ),
        }

    def __repr__(self) -> str:
        return (
            "MotzkinPathsStartingWithU(crossing_avoids={}, "
            "crossing_contains={})".format(repr(self.avoids), repr(self.contains))
        )

    def __str__(self, extra: str = "") -> str:
        return MotzkinPaths.__str__(self, extra="U")


if __name__ == "__main__":
    avoids = ["UUU"]
    contains = [["HU"]]
    m = MotzkinPaths(avoids, contains)
    mu = MotzkinPathsStartingWithU(avoids, contains)
    mh = MotzkinPathsStartingWithH(avoids, contains)
    print(m)
    print(mu)
    print(mh)

    for i in range(1, 30):
        ch = 0
        cu = 0
        for o in m.objects_of_size(i):
            if o[0] == "U":
                cu += 1
            if o[0] == "H":
                ch += 1
        print("-", i, "-")
        print(ch, cu)
        print(len(list(mh.objects_of_size(i))), len(list(mu.objects_of_size(i))))
