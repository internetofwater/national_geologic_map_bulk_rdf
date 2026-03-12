from pathlib import Path
import requests
from zipfile import ZipFile

PATH_TO_GPGK = (
    Path(__file__).parent.parent
    / "USGS_DR-1210_full-db_V1"
    / "ngs_full_2025_v1"
    / "ngs_full_2025_v1-database"
    / "ngs_full_2025_v1.gpkg"
)


def download_if_not_exists() -> Path:
    if PATH_TO_GPGK.exists():
        return PATH_TO_GPGK

    url = "https://ngmdb.usgs.gov/docs/gis/USGS_DR-1210_full-db_V1.zip"
    zip_path = PATH_TO_GPGK.parent.parent.parent / "USGS_DR-1210_full-db_V1.zip"

    # Ensure parent directories exist
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    # Stream download to file
    if not zip_path.exists():
        print(f"Downloading {url} to {zip_path} ...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1 MB chunks
                    if chunk:
                        f.write(chunk)
        print("Download complete.")

    # Extract only the .gpkg file
    print(f"Extracting .gpkg from {zip_path} ...")
    with ZipFile(zip_path, "r") as zf:
        for file_info in zf.infolist():
            if file_info.filename.endswith(".gpkg"):
                # Extract to the expected folder
                target_dir = PATH_TO_GPGK.parent
                target_dir.mkdir(parents=True, exist_ok=True)
                zf.extract(file_info, target_dir.parent.parent.parent)
                break
        else:
            raise FileNotFoundError(".gpkg file not found in the zip")

    if not PATH_TO_GPGK.exists():
        raise FileNotFoundError(f"Failed to extract {PATH_TO_GPGK}")

    print(f"Data ready at {PATH_TO_GPGK}")
    return PATH_TO_GPGK

def row_to_jsonld(): ...