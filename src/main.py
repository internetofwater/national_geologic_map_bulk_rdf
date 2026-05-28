
# %%
from geopandas import gpd

from lib import download_if_not_exists, row_to_jsonld
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():

    files = download_if_not_exists()

    for file in files:
        sql_query = """
        SELECT * FROM MapUnitPolys
        """


        polys = gpd.read_file(file, sql=sql_query)

        geologic_data = gpd.read_file(file, layer="Source_DescriptionOfMapUnits")

        df = polys.merge(geologic_data, on="Source_MapUnit", how="left")

        df_clean = df[
            [
                "MapUnit",
                "Name",
                "FullName",
                "Age",
                "Description",
                "GeoMaterial",
                "GeoMaterialConfidence",
                "geometry",
            ]
        ]

        for row in df_clean.iterrows():
            print(row_to_jsonld(row))


if __name__ == "__main__":
    main()

# %%
