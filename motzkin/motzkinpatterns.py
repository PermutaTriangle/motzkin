"""This module contains a class for Motzkin paths, patterns and crossing
patterns."""
from itertools import product
from typing import Dict, FrozenSet, Iterable, Iterator, List, Set, Tuple, Union

__all__ = ["MotzkinPath", "CrossingPattern"]


class MotzkinPath(tuple):
    def __new__(cls, path: Iterable[str] = tuple(), pattern: bool = False):
        return tuple.__new__(cls, path)

    def __init__(self, path: Iterable[str] = tuple(), pattern: bool = False):
        """If pattern is set to True, then it has only to be a word over
        {U, D, H}, otherwise it must be a valid Motzkin path."""
        if not all(l in ("U", "D", "H") for l in path):
            raise ValueError('All letters must be "U", "D", or "H"')
        self.pattern = bool(pattern)
        if not pattern:
            height = 0
            for l in path:
                if l == "U":
                    height += 1
                elif l == "D":
                    height -= 1
                if height < 0:
                    raise ValueError("Path goes below x-axis.")
            if height:
                raise ValueError("Path does not end on x-axis.")

    def avoids(self, other: Union["CrossingPattern", "MotzkinPath"]) -> bool:
        return not self.contains(other)

    def contains(self, other: Union["CrossingPattern", "MotzkinPath"]) -> bool:
        """Return True if self contains other as a not necessarily consecutive
        subword."""
        if isinstance(other, CrossingPattern):
            return other.contained_in(self)
        else:
            if len(self) < len(other):
                return False

            def recursive_check(path, patt):
                patt = list(reversed(other))
                while patt and path:
                    curr = patt.pop()
                    for i, l in enumerate(path):
                        if l == curr:
                            path = path[i + 1 :]
                            break
                    else:
                        return False
                return not patt

            return recursive_check(self, other)

    def heights(self) -> List[int]:
        """Return a list corresponding to the heights of the Motzkin path."""
        height = 0
        heights = [0]
        for l in self:
            if l == "U":
                height += 1
            elif l == "D":
                height -= 1
            heights.append(height)
        return heights

    def is_motzkin_path(self) -> bool:
        height = 0
        for l in self:
            if l == "U":
                height += 1
            elif l == "D":
                height -= 1
            if height < 0:
                return False
        return height == 0

    MINIMAL_SET_CACHE: Dict["MotzkinPath", FrozenSet["MotzkinPath"]] = {}

    def minimal_set_for_avoidance(self) -> FrozenSet["MotzkinPath"]:
        if self not in MotzkinPath.MINIMAL_SET_CACHE:
            if not self.pattern or self.is_motzkin_path():
                MotzkinPath.MINIMAL_SET_CACHE[self] = frozenset([self])
            else:
                seen = set()
                to_process = set([self])
                minimal_paths: Set["MotzkinPath"] = set()
                while to_process:
                    curr = to_process.pop()
                    seen.add(curr)
                    if any(p in curr for p in minimal_paths):
                        continue
                    if curr.is_motzkin_path():
                        minimal_paths.add(curr)
                        continue
                    heights = curr.heights()
                    below_indices = [
                        i for i, v in enumerate(heights) if v < 0 and curr[i - 1] == "D"
                    ]
                    if below_indices:
                        # add U to push above x-axis
                        last_below = below_indices[-1]
                        for j in range(last_below):
                            new_path = MotzkinPath(
                                curr[:j] + ("U",) + curr[j:], pattern=True
                            )
                            if new_path not in seen:
                                to_process.add(new_path)
                    else:
                        # need to consider adding D as it doesn't end on the x-axis
                        zero_indices = [i for i, v in enumerate(heights) if v == 0]
                        last_zero = zero_indices[-1]
                        for k in range(last_zero + 1, len(curr) + 1):
                            new_path = MotzkinPath(
                                curr[:k] + ("D",) + curr[k:], pattern=True
                            )
                            if new_path not in seen:
                                to_process.add(new_path)
                minimal_set: Set[MotzkinPath] = set()
                for av in sorted(minimal_paths, key=len):
                    if all(p not in av for p in minimal_set):
                        minimal_set.add(av)
                MotzkinPath.MINIMAL_SET_CACHE[self] = frozenset(minimal_set)
        return MotzkinPath.MINIMAL_SET_CACHE[self]

    def minimal_set_for_avoidance_rec(self) -> FrozenSet["MotzkinPath"]:
        if self not in MotzkinPath.MINIMAL_SET_CACHE:
            if self.is_motzkin_path():
                minimal_set = set([self])
            else:
                heights = self.heights()
                below_indices = [
                    i for i, v in enumerate(heights) if v < 0 and self[i - 1] == "D"
                ]
                one_level_higher = set()
                if below_indices:
                    # add U to push above x-axis
                    last_below = below_indices[-1]
                    for j in range(last_below):
                        new_path = MotzkinPath(
                            self[:j] + ("U",) + self[j:], pattern=True
                        )
                        one_level_higher.add(new_path)
                else:
                    # need to consider adding D as it doesn't end on the x-axis
                    zero_indices = [i for i, v in enumerate(heights) if v == 0]
                    last_zero = zero_indices[-1]
                    for k in range(last_zero + 1, len(self) + 1):
                        new_path = MotzkinPath(
                            self[:k] + ("D",) + self[k:], pattern=True
                        )
                        one_level_higher.add(new_path)
                avoids = set.union(
                    *[set(p.minimal_set_for_avoidance_rec()) for p in one_level_higher]
                )
                minimal_set = set()
                for av in sorted(avoids, key=len):
                    if all(p not in av for p in minimal_set):
                        minimal_set.add(av)
            MotzkinPath.MINIMAL_SET_CACHE[self] = frozenset(minimal_set)
        return MotzkinPath.MINIMAL_SET_CACHE[self]

    def split(self) -> Tuple["MotzkinPath", "MotzkinPath"]:
        """Return a pair of Motzkin paths where the first is up to the first
        return and the second is the Motzkin path after the first return."""
        if MotzkinPath("U", pattern=True) not in self:
            return self, MotzkinPath()
        height = 0
        for i, l in enumerate(self):
            if l == "U":
                height += 1
            elif l == "D":
                height -= 1
            else:
                continue
            if height == 0:
                # first return
                return MotzkinPath(self[: i + 1]), MotzkinPath(self[i + 1 :])
        raise ValueError("something went wrong.")

    def to_jsonable(self) -> Tuple[str, ...]:
        return tuple(self)

    @classmethod
    def from_dict(cls, patt: Iterable[str]) -> "MotzkinPath":
        return MotzkinPath(patt)

    def _ascii_plot(self) -> str:
        height = 0
        res = [[" " for _ in range(len(self))] for _ in range(len(self))]
        for i, l in enumerate(self):
            if l == "D":
                height -= 1
            res[height][i] = "/" if l == "U" else "\\" if l == "D" else "_"
            if l == "U":
                height += 1
        return "\n".join(
            "".join(i for i in L) for L in reversed(res) if any(l != " " for l in L)
        )

    def __contains__(self, other) -> bool:
        if isinstance(other, (CrossingPattern, MotzkinPath)):
            return self.contains(other)
        print(self, type(self))
        print(other, type(other))
        raise NotImplementedError

    def __add__(self, other: Tuple[str, ...]) -> "MotzkinPath":
        other = self.__class__(other)
        return MotzkinPath(tuple(self) + tuple(other))

    def __lt__(self, other) -> bool:
        if isinstance(other, MotzkinPath):
            return (len(self), tuple(self)) < (len(other), tuple(other))
        raise NotImplementedError

    def __repr__(self) -> str:
        return "MotzkinPath({})".format(repr(tuple(self)))

    def __str__(self) -> str:
        if not self:
            return "\u03BB"
        return "".join(l for l in self)


class CrossingPattern(object):
    def __init__(self, left: Tuple[str, ...], right: Tuple[str, ...]):
        if not all(l in ("U", "D", "H") for l in left) or not all(
            l in ("U", "D", "H") for l in right
        ):
            raise ValueError('All letters must be "U", "D", or "H"')
        self.left = MotzkinPath(left, pattern=True)
        self.right = MotzkinPath(right, pattern=True)

    def avoided_by(self, path: MotzkinPath) -> bool:
        return not self.contained_in(path)

    def contained_in(self, path: MotzkinPath) -> bool:
        """Return True if the Motzkin path contains left before its first
        return and right after its first return."""
        before, after = path.split()
        return self.left in before and self.right in after

    def is_left_localised(self) -> bool:
        return not self.right

    def is_right_localised(self) -> bool:
        return not self.left

    def is_localised(self) -> bool:
        return self.is_left_localised() or self.is_right_localised()

    def motzkin_crossings(self) -> List["CrossingPattern"]:
        """Returns the minimal set of crossing patterns such the left and the
        right are both Motzkin paths."""
        return [
            CrossingPattern(l, r)
            for l, r in product(
                self.left.minimal_set_for_avoidance(),
                self.right.minimal_set_for_avoidance(),
            )
        ]

    def minimal_set_for_avoidance(self) -> FrozenSet["CrossingPattern"]:
        return frozenset(self.motzkin_crossings())

    def to_jsonable(self):
        return {"left": self.left.to_jsonable(), "right": self.right.to_jsonable()}

    @classmethod
    def from_dict(cls, d: dict):
        left = MotzkinPath.from_dict(d.pop("left"))
        right = MotzkinPath.from_dict(d.pop("right"))
        return CrossingPattern(left, right)

    def __contains__(self, other) -> bool:
        if isinstance(other, CrossingPattern):
            return other.left in self.left and other.right in self.right
        raise NotImplementedError

    @classmethod
    def all_crossing_patterns(self, patt: MotzkinPath) -> Iterator["CrossingPattern"]:
        if not all(l in ("U", "D", "H") for l in patt):
            raise ValueError('All letters must be "U", "D", or "H"')
        for i in range(len(patt) + 1):
            yield CrossingPattern(patt[:i], patt[i:])

    def __eq__(self, other) -> bool:
        if isinstance(other, CrossingPattern):
            return (
                type(self) == type(other)
                and self.left == other.left
                and self.right == other.right
            )
        raise NotImplementedError

    def __bool__(self) -> bool:
        return bool(self.left) or bool(self.right)

    def __len__(self) -> int:
        return len(self.left) + len(self.right)

    def __lt__(self, other) -> bool:
        if isinstance(other, CrossingPattern):
            return (
                len(self.left),
                tuple(self.left),
                len(self.right),
                tuple(self.right),
            ) < (
                len(other.left),
                tuple(other.left),
                len(other.right),
                tuple(other.right),
            )
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(hash(self.left) + hash(self.right))

    def __repr__(self) -> str:
        return "CrossingPattern({}, {})".format(
            repr(tuple(self.left)), repr(tuple(self.right))
        )

    def __str__(self) -> str:
        return "{}-{}".format(str(self.left), str(self.right))


if __name__ == "__main__":
    patt = MotzkinPath("HHUUDUUHUU", True)
    patt = MotzkinPath("UUDU", True)
    # patt = MotzkinPath("UDDUUUDUD", True)
    # patt = MotzkinPath("DDUUDU", True)
    # patt = MotzkinPath("DD", True)
    b = patt.minimal_set_for_avoidance()
    print(
        "The minimal paths for {} were: {}".format(patt, ", ".join(str(p) for p in b))
    )

    # # for computing the actual basis experimentally
    # from motzkinpaths import MotzkinPaths
    # actual_basis = set()
    # for i in range(115):
    #     for p in MotzkinPaths(actual_basis).objects_of_length(i):
    #         if patt in p:
    #             print(p)
    #             if all(q not in p for q in actual_basis):
    #                 actual_basis.add(p)
    #     print(len(actual_basis))

    # test for minimality
    b = list(b)
    for i, p in enumerate(b):
        for q in b[i + 1 :]:
            assert (p not in q) and (q not in p)

    # # test for correct avoidance
    from motzkinpaths import MotzkinPaths

    m1 = MotzkinPaths()
    m2 = MotzkinPaths(b)
    for i in range(100):
        s1 = set([p for p in m1.objects_of_length(i) if patt not in p])
        s2 = set(m2.objects_of_length(i))
        print(len(s1), len(s2))
        if s1 != s2:
            for p in s1.union(s2) - s1.intersection(s2):
                if p in s1:
                    print(p, "in s1")
                if p in s2:
                    print(p, "in s2")
            break
