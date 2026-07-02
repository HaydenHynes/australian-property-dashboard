"""
Download service.

Provides reusable functions for downloading files from external data sources.
"""

from pathlib import Path
from urllib.parse import urlparse

import requests

REQUEST_TIMEOUT_SECONDS = 30
CHUNK_SIZE_BYTES = 8192

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}

def validate_url(url: str) -> None:
    """Validate that a URL has a supported HTTP or HTTPS scheme."""
    parsed_url = urlparse(url)

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}")

    if not parsed_url.netloc:
        raise ValueError("URL must include a valid domain.")


def ensure_directory_exists(directory: Path) -> None:
    """Create a directory if it does not already exist."""
    directory.mkdir(parents=True, exist_ok=True)


def download_file(
    url: str,
    destination_dir: Path,
    filename: str,
    overwrite: bool = False,
) -> Path:
    """Download a file from a URL and save it to a destination directory."""
    validate_url(url)
    ensure_directory_exists(destination_dir)

    destination_path = destination_dir / filename
    
    if destination_path.exists() and not overwrite:
      raise FileExistsError(
          f"The file '{destination_path.name}' already exists. "
          "Pass overwrite=True to replace it."
      )

    with requests.get(
    url,
    timeout=REQUEST_TIMEOUT_SECONDS,
    stream=True,
    headers=REQUEST_HEADERS,
) as response:
      response.raise_for_status()

      with destination_path.open("wb") as file:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE_BYTES):
              if chunk:
                  file.write(chunk)

    return destination_path