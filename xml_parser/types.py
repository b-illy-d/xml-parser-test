import os
from typing import IO, Iterator, Tuple, Union

from lxml import etree

_PathLike = Union[str, os.PathLike[str]]
_StreamLike = IO[str] | IO[bytes]
ParseEvent = Tuple[str, etree._Element]
ParseStream = Iterator[ParseEvent]
