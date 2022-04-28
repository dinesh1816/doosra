import sys
from _typeshed import SupportsRead
from typing import Any, Callable, Generic, MutableMapping, Pattern, Text, TypeVar, overload
from typing_extensions import TypeAlias

_MutableMappingT = TypeVar("_MutableMappingT", bound=MutableMapping[str, Any])

if sys.version_info >= (3, 0):
    from pathlib import PurePath

    FNFError = FileNotFoundError
    _PathLike: TypeAlias = str | bytes | PurePath
else:
    FNFError = IOError
    _PathLike: TypeAlias = Text

TIME_RE: Pattern[str]

class TomlDecodeError(ValueError):
    msg: str
    doc: str
    pos: int
    lineno: int
    colno: int
    def __init__(self, msg: str, doc: str, pos: int) -> None: ...

class CommentValue:
    val: Any
    comment: str
    def __init__(self, val: Any, comment: str, beginline: bool, _dict: type[MutableMapping[str, Any]]) -> None: ...
    def __getitem__(self, key: Any) -> Any: ...
    def __setitem__(self, key: Any, value: Any) -> None: ...
    def dump(self, dump_value_func: Callable[[Any], str]) -> str: ...

@overload
def load(
    f: _PathLike | list[Any] | SupportsRead[Text],  # list[_PathLike] is invariance
    _dict: type[_MutableMappingT],
    decoder: TomlDecoder[_MutableMappingT] | None = ...,
) -> _MutableMappingT: ...
@overload
def load(
    f: _PathLike | list[Any] | SupportsRead[Text],  # list[_PathLike] is invariance
    _dict: type[dict[str, Any]] = ...,
    decoder: TomlDecoder[dict[str, Any]] | None = ...,
) -> dict[str, Any]: ...
@overload
def loads(s: Text, _dict: type[_MutableMappingT], decoder: TomlDecoder[_MutableMappingT] | None = ...) -> _MutableMappingT: ...
@overload
def loads(s: Text, _dict: type[dict[str, Any]] = ..., decoder: TomlDecoder[dict[str, Any]] | None = ...) -> dict[str, Any]: ...

class InlineTableDict: ...

class TomlDecoder(Generic[_MutableMappingT]):
    _dict: type[_MutableMappingT]
    @overload
    def __init__(self, _dict: type[_MutableMappingT]) -> None: ...
    @overload
    def __init__(self: TomlDecoder[dict[str, Any]], _dict: type[dict[str, Any]] = ...) -> None: ...
    def get_empty_table(self) -> _MutableMappingT: ...
    def get_empty_inline_table(self) -> InlineTableDict: ...  # incomplete python/typing#213
    def load_inline_object(
        self, line: str, currentlevel: _MutableMappingT, multikey: bool = ..., multibackslash: bool = ...
    ) -> None: ...
    def load_line(
        self, line: str, currentlevel: _MutableMappingT, multikey: bool | None, multibackslash: bool
    ) -> tuple[bool | None, str, bool] | None: ...
    def load_value(self, v: str, strictly_valid: bool = ...) -> tuple[Any, str]: ...
    def bounded_string(self, s: str) -> bool: ...
    def load_array(self, a: str) -> list[Any]: ...
    def preserve_comment(self, line_no: int, key: str, comment: str, beginline: bool) -> None: ...
    def embed_comments(self, idx: int, currentlevel: _MutableMappingT) -> None: ...

class TomlPreserveCommentDecoder(TomlDecoder[_MutableMappingT]):
    saved_comments: dict[int, tuple[str, str, bool]]