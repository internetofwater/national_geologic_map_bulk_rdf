from pathlib import Path
from geopandas import gpd


PATH_TO_GPGK = (
    Path(__file__).parent.parent
    / "USGS_DR-1210_full-db_V1"
    / "ngs_full_2025_v1"
    / "ngs_full_2025_v1-database"
    / "ngs_full_2025_v1.gpkg"
)


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
    assert columns == gpd.list_layers(PATH_TO_GPGK).to_dict(orient="list")["name"]


if __name__ == "__main__":
    main()
