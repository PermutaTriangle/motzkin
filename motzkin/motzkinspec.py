from typing import Iterable

from comb_spec_searcher import CombinatorialSpecificationSearcher

from .motzkinpaths import MotzkinPaths
from .motzkinpatterns import MotzkinPath
from .strategies import MotzkinPack

__all__ = "MotzkinSpecificationFinder"


class MotzkinSpecificationFinder(CombinatorialSpecificationSearcher):
    pack = MotzkinPack

    def __init__(self, patterns: Iterable[Iterable[str]], **kwargs):
        patterns = tuple(MotzkinPath(patt, pattern=True) for patt in patterns)
        start_class = MotzkinPaths(patterns)
        super().__init__(start_class, MotzkinPack, **kwargs)
