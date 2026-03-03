#!/bin/sh

cd $(dirname $0)

sqlite3 ../USGS_DR-1210_full-db_V1/ngs_full_2025_v1/ngs_full_2025_v1-database/ngs_full_2025_v1.gpkg \
"SELECT table_name FROM gpkg_contents WHERE data_type='features';" \
| while read t; do echo "$t $(sqlite3 ../USGS_DR-1210_full-db_V1/ngs_full_2025_v1/ngs_full_2025_v1-database/ngs_full_2025_v1.gpkg "SELECT COUNT(*) FROM \"$t\";")"; done \
| sort -k2 -nr