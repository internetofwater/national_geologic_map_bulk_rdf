#!/bin/sh

cd $(dirname $0)

DB="../USGS_DR-1210_full-db_V1/ngs_full_2025_v1/ngs_full_2025_v1-database/ngs_full_2025_v1.gpkg"

echo "layer_name feature_count column_count"

sqlite3 "$DB" "SELECT table_name FROM gpkg_contents WHERE data_type='features';" \
| while read t; do
    feature_count=$(sqlite3 "$DB" "SELECT COUNT(*) FROM \"$t\";")
    column_count=$(sqlite3 "$DB" "PRAGMA table_info(\"$t\");" | wc -l)
    echo "$t $feature_count $column_count"
done | sort -k2 -nr