# Copyright 2026 Lincoln Institute of Land Policy
# SPDX-License-Identifier: MIT

import argparse
import json
import logging

import geopandas as gpd

from lib import COLUMNS_TO_KEEP, download_if_not_exists, row_to_jsonld

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

TEST_ROW_COUNT = 100


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Template National Geologic Map rows as newline-delimited JSON-LD.",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help=f"Emit at most {TEST_ROW_COUNT} rows for quick testing.",
    )
    parser.add_argument(
        "--head",
        action="store_true",
        help="Show the first few rows of each gpkg",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.head:
        files = download_if_not_exists()
        for name, path in files.items():
            gdf = gpd.read_file(path, layer="MapUnitPolys")
            print(name)
            print(gdf.head(5))
            print()
        return

    row_limit = TEST_ROW_COUNT if args.test_mode else None
    rows_emitted = 0

    files = download_if_not_exists()

    for name, path in files.items():
        polys = gpd.read_file(path, layer="MapUnitPolys")

        geologic_data = gpd.read_file(path, layer="Source_DescriptionOfMapUnits")

        df = polys.merge(
            geologic_data,
            on="Source_MapUnit",
            how="left",
            suffixes=("_poly", "_unit"),
        )

        df_clean = df[list(COLUMNS_TO_KEEP)]
        df_clean["Symbol"] = df_clean["Symbol_poly"]
        df_clean = df_clean.drop(columns=["Symbol_poly"])
        df_clean.to_crs(epsg=4326, inplace=True)

        columns = [str(column) for column in df_clean.columns]
        for values in df_clean.itertuples(index=False, name=None):
            if row_limit is not None and rows_emitted >= row_limit:
                return
            row = dict(zip(columns, values, strict=True))
            jsonld = row_to_jsonld(row, name)
            print(json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")))
            rows_emitted += 1
        LOGGER.info(f"Finished templating {name} with {rows_emitted} rows")


if __name__ == "__main__":
    main()
