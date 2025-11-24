from typing import Protocol, runtime_checkable


@runtime_checkable
class StreamLike(Protocol):
    def read(self, *args, **kwargs) -> bytes: ...
    def close(self) -> None: ...
