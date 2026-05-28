from pathlib import Path
import requests
from zipfile import ZipFile
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


GEOLOGY_MAP_DATA_DIR = Path(__file__).parent / "data"

GDB_URLS = {
    "earth_surface_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3436&pid=118545",
    "quaternary_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3437&pid=118545",
    "pre-quaternary_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3438&pid=118545",
    "precambrian_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3598&pid=118545",
}


def _download_file(url: str, out_path: Path):
    if out_path.exists():
        return

    LOGGER.info(f"Downloading {url} → {out_path}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
    LOGGER.info("Download complete.")


def _extract_zip(zip_path: Path, extract_to: Path):
    LOGGER.info(f"Extracting {zip_path} → {extract_to}")
    with ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_to)
    LOGGER.info("Extraction complete.")


def download_if_not_exists() -> dict[str, Path]:
    GEOLOGY_MAP_DATA_DIR.mkdir(parents=True, exist_ok=True)

    gdb_paths: dict[str, Path] = {}

    for name, url in GDB_URLS.items():
        zip_path = GEOLOGY_MAP_DATA_DIR / f"{name}.zip"
        extract_dir = GEOLOGY_MAP_DATA_DIR / name

        if zip_path.exists() or extract_dir.exists():
            LOGGER.info(f"Skipping downloading {name} since it already exists")
        else:     
            _download_file(url, zip_path)

        # Extract if needed
        if not extract_dir.exists():
            _extract_zip(zip_path, extract_dir)

        # Find the .gdb folder
        gdb_dirs = list(extract_dir.rglob("*.gdb"))
        if not gdb_dirs:
            raise FileNotFoundError(f"No .gdb found in {extract_dir}")

        assert len(gdb_dirs) == 1, "More than one .gdb found"

        # Usually one per archive, but handle safely
        gdb_paths[name] = gdb_dirs[0]

        # delete the zip file since it is no longer needed
        if zip_path.exists():
            zip_path.unlink()

    if not gdb_paths:
        raise RuntimeError("No GDBs were found after extraction")

    return gdb_paths


def row_to_jsonld(): ...
