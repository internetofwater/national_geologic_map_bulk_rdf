# Copyright 2026 Lincoln Institute of Land Policy
# SPDX-License-Identifier: MIT

import logging
from collections.abc import Mapping
from pathlib import Path
from zipfile import ZipFile
import pandas as pd

import requests

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"FullName", "geometry", "MapUnitPolys_ID", "Description"}

OPTIONAL_COLUMNS = {
    "MapUnit",
    "Name",
    "Age",
    "GeoMaterial",
    "GeoMaterialConfidence",
    "IdentityConfidence",
    "Symbol_poly",
    "DataSourceID",
    "MapSourceID",
    "Source_MapUnit",
}

COLUMNS_TO_KEEP = REQUIRED_COLUMNS | OPTIONAL_COLUMNS

GEOLOGY_MAP_DATA_DIR = Path(__file__).parent / "data"

GDB_URLS = {
    "earth_surface_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3436&pid=118545",
    "quaternary_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3437&pid=118545",
    "pre-quaternary_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3438&pid=118545",
    "precambrian_geology": "https://ngmdb.usgs.gov/ngm-bin/gems_download.pl?id=3598&pid=118545",
}


def _download_file(url: str, out_path: Path) -> None:
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


def _extract_zip(zip_path: Path, extract_to: Path) -> None:
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


def row_to_jsonld(row: Mapping[str, object], source_name: str):
    polygon_id = row.get("MapUnitPolys_ID")

    if not isinstance(polygon_id, str):
        raise ValueError("MapUnitPolys_ID is required for JSON-LD identifiers")

    identifier = f"{source_name}:{polygon_id}"

    # base geometry
    shapely_obj = row.get("geometry")
    assert shapely_obj is not None

    name = row.get("FullName")
    assert name, "FullName is required for JSON-LD names"

    document = {
        "@context": {
            "@vocab": "https://schema.org/",
            "gsp": "http://www.opengis.net/ont/geosparql#",
        },
        "@id": f"https://geoconnex.us/usgs/national-geologic-map/{identifier}",
        "@type": "Place",
        "identifier": identifier,
        "gsp:hasGeometry": {
            "@type": "http://www.opengis.net/ont/sf#Polygon",
            "gsp:asWKT": {"@type": "gsp:wktLiteral", "@value": shapely_obj.wkt},  # pyright: ignore[reportAttributeAccessIssue]
            "gsp:crs": {"@id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
        },
        "name": name,
        "variableMeasured": [],
    }
    description = row.get("Description")
    if (
        description is not None
        and not pd.isna(description)  # type: ignore
        and str(description).strip().lower() not in {"none", "nan", ""}
    ):
        document["description"] = str(description)

    for column in OPTIONAL_COLUMNS:
        # name is a special case; we don't really
        # want to include this as a variableMeasured
        # but it is nonetheless an optional column
        if column == "name":
            continue
        value = row.get(column)
        if value is None or value == "" or pd.isna(value):   # type: ignore
            continue
        document["variableMeasured"].append(
            {"@type": "PropertyValue", "name": column, "value": value}
        )

    return document
