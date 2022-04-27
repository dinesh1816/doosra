import sys
from _typeshed import Self, StrOrBytesPath
from cProfile import Profile as _cProfile
from profile import Profile
from typing import IO, Any, Iterable, overload
from typing_extensions import Literal, TypeAlias

if sys.version_info >= (3, 9):
    __all__ = ["Stats", "SortKey", "FunctionProfile", "StatsProfile"]
elif sys.version_info >= (3, 7):
    __all__ = ["Stats", "SortKey"]
else:
    __all__ = ["Stats"]

_Selector: TypeAlias = str | float | int

if sys.version_info >= (3, 7):
    from enum import Enum

    class SortKey(str, Enum):
        CALLS: str
        CUMULATIVE: str
        FILENAME: str
        LINE: str
        NAME: str
        NFL: str
        PCALLS: str
        STDNAME: str
        TIME: str

if sys.version_info >= (3, 9):
    from dataclasses import dataclass

    @dataclass(unsafe_hash=True)
    class FunctionProfile:
        ncalls: int
        tottime: float
        percall_tottime: float
        cumtime: float
        percall_cumtime: float
        file_name: str
        line_number: int
    @dataclass(unsafe_hash=True)
    class StatsProfile:
        total_tt: float
        func_profiles: dict[str, FunctionProfile]

_SortArgDict: TypeAlias = dict[str, tuple[tuple[tuple[int, int], ...], str]]

class Stats:
    sort_arg_dict_default: _SortArgDict
    def __init__(
        self: Self,
        __arg: None | str | Profile | _cProfile = ...,
        *args: None | str | Profile | _cProfile | Self,
        stream: IO[Any] | None = ...,
    ) -> None: ...
    def init(self, arg: None | str | Profile | _cProfile) -> None: ...
    def load_stats(self, arg: None | str | Profile | _cProfile) -> None: ...
    def get_top_level_stats(self) -> None: ...
    def add(self: Self, *arg_list: None | str | Profile | _cProfile | Self) -> Self: ...
    def dump_stats(self, filename: StrOrBytesPath) -> None: ...
    def get_sort_arg_defs(self) -> _SortArgDict: ...
    @overload
    def sort_stats(self: Self, field: Literal[-1, 0, 1, 2]) -> Self: ...
    @overload
    def sort_stats(self: Self, *field: str) -> Self: ...
    def reverse_order(self: Self) -> Self: ...
    def strip_dirs(self: Self) -> Self: ...
    def calc_callees(self) -> None: ...
    def eval_print_amount(self, sel: _Selector, list: list[str], msg: str) -> tuple[list[str], str]: ...
    if sys.version_info >= (3, 9):
        def get_stats_profile(self) -> StatsProfile: ...

    def get_print_list(self, sel_list: Iterable[_Selector]) -> tuple[int, list[str]]: ...
    def print_stats(self: Self, *amount: _Selector) -> Self: ...
    def print_callees(self: Self, *amount: _Selector) -> Self: ...
    def print_callers(self: Self, *amount: _Selector) -> Self: ...
    def print_call_heading(self, name_size: int, column_title: str) -> None: ...
    def print_call_line(self, name_size: int, source: str, call_dict: dict[str, Any], arrow: str = ...) -> None: ...
    def print_title(self) -> None: ...
    def print_line(self, func: str) -> None: ...
