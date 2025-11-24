import os
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from .types import StreamLike

_GCS_HTTP_BASE = "https://storage.googleapis.com"


def read_stdin() -> StreamLike:
    """Read XML data from stdin and return the parser."""
    return sys.stdin.buffer


def read_file(path: str) -> StreamLike:
    """Read XML data from a local file path and return the parser."""
    file_path = os.fspath(path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    if not os.path.isfile(file_path):
        raise IsADirectoryError(file_path)

    if file_path is None:
        raise FileNotFoundError("Example XML file not found.")
    return open(file_path, "rb")


def _normalize_gcs_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return url
    """TODO: Support gs:// scheme if needed in the future."""
    raise ValueError(f"Unsupported scheme for GCS url: {url}")


def read_gcs(url: str) -> StreamLike:
    """Read XML data from a public Google Cloud Storage URL."""
    normalized_url = _normalize_gcs_url(url)
    try:
        response = urlopen(normalized_url)  # noqa: S310 - Public data only
    except ValueError as e:
        raise ValueError(f"Invalid URL {normalized_url}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error while reading GCS URL {normalized_url}: {e}")

    return response
