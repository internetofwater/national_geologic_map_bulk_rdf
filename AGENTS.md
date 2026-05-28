# AGENTS.md

## Project Overview

This project takes the items output from a the National Geology Map geodatabase and templates into jsonld rdf data. It then prints that data to standard out. The standard out should be exclusively newline delimited jsonld. Any other logs should be sent to stderr. The final output of this is a docker container that can be pulled and run as a way of packaging rdf data in a portable way. Use mainly schema.org and geosparql for the rdf vocabulary. OGR and/or GDAL can be used to investigate the source gdb files which exist in the src/data directory.

## Code style

- Use as minimal dependencies are possible. Do templating by using dicts which serialize into json. Do not use raw string templating like jinja2. 
- Statically type everything. Do not use kwargs or varargs.
- Do not use many small functions with `_` in the name. 

## Setup commands
- Install deps: `uv sync --all-extras`
- Run tests: `uv run pytest`

# Testing Instructions

- Run `prek run --all-files`
- Run the script with 100 items and ensure it templates properly by using a `--test-mode` flag.
- Test a subset of the jsonld data using the cli command `nabu shacl -` and pipe in in the jsonld as stdin. Don't test all files, but make sure the rdf is generally compatible with the shape.
- To find the shacl shape you can run `nabu shacl --print-shape`
