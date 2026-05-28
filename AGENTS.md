# AGENTS.md

## Project Overview

This project takes the items output from a the National Geology Map geodatabase and templates into jsonld rdf data. It then prints that data to standard out. The standard out should be exclusively newline delimited jsonld. Any other logs should be sent to stderr. The final output of this is a docker container that can be pulled and run as a way of packaging rdf data in a portable way. Use mainly schema.org for the rdf vocabulary.

## Code style

- Use as minimal dependencies are possible. Do templating by using dicts which serialize into json. Do not use raw string templating like jinja2. 
- Statically type everything. Do not use kwargs or varargs.
- Do not use many small functions with `_` in the name. 

## Setup commands
- Install deps: `uv sync --all-extras`
- Run tests: `uv run pytest`

# Testing Instructions

- Run `prek run --all-files`
- Run the script with 50k items and ensure it templates properly by using a `--test-mode` flag.
