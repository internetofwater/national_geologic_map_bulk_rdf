
# %%
from geopandas import gpd

from lib import download_if_not_exists

# %%
def main():
    columns = [
        "source_mapsourcepolys",
        "source_mapunitpolys",
        "source_overlaypolys",
        "source_datasourcepolys",
        "source_mapunitoverlaypolys",
        "source_cartographiclines",
        "source_geologiclines",
        "source_isovaluelines",
        "source_genericpoints",
        "source_geochronpoints",
        "source_mapunitpoints",
        "source_orientationpoints",
        "source_mapunitlines",
        "source_contactsandfaults",
        "synthesis_mapunitlines",
        "synthesis_mapunitpolys",
        "synthesis_contactsandfaults",
        "synthesis_geologiclines",
        "source_mapsources",
        "source_datasources",
        "source_descriptionofmapunits",
        "synthesis_descriptionofmapunits",
        "synthesis_to_source_units",
        "synthesis_synthesissources",
        "vocabularies_vocabularysources",
        "vocabularies_glossary",
        "vocabularies_lithologydict",
        "vocabularies_resolutions",
        "vocabularies_geomaterialdict",
        "vocabularies_proportiondict",
        "vocabularies_confidencedict",
        "vocabularies_agedict",
        "vocabularies_geolayers",
        "vocabularies_search_attributes",
        "vocabularies_search_operations",
        "vocabularies_symbol_lookup",
        "assignments_age",
        "assignments_lithology",
    ]

    path_to_gpkg = download_if_not_exists()

    assert columns == gpd.list_layers(path_to_gpkg).to_dict(orient="list")["name"]


if __name__ == "__main__":
    main()

# %%
