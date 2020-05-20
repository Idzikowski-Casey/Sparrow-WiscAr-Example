# Sparrow for the WiscAr lab

This installation of Sparrow powers the WiscAr lab at the University of Wisconsin.

## Installation

Currently, Sparrow is included as a [Git Submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
This pins Sparrow to a particular version that is supported by the WiscAr lab.

The installation steps closely follow those
for [setting up Sparrow by itself](https://sparrow-data.org/installation/),
but differ slightly because Sparrow is itself a submodule.
First, clone this repository from Github. Then, within the created
directory, run `git submodule update --init --recursive`. This will
check out Sparrow and all of its submodules in a single step.

As in the general instructions, linking the `sparrow` command-line executable
onto your path with `sudo ln -s Sparrow/bin/sparrow /usr/local/bin` will allow
you to run the Sparrow command-line application.

The `sparrow-config.sh` file in this repository contains configuration for WiscAr's
version of Sparrow. It will be automatically sourced anytime you run `sparrow`
in this repository's directory or a subdirectory.
You will need to create a file `sparrow-config.overrides.sh` in this directory
containing application secrets:
```
export MAPBOX_API_TOKEN=<your-api-token>
export SPARROW_SECRET_KEY=<example>
```
You can also override other Sparrow environment variables in this file.

## Updating Sparrow

Sparrow can be updated by checking out the desired version *within the Sparrow
submodule*, and running `git submodule update --init --recursive` to make sure
any dependencies stay in sync. When updating, you may need to run a
database migration [more info on that soon].

## Getting data

### Restoring from a database dump

The state of an existing Sparrow installation can be restored using the command
`sparrow db-import <your-database.pg-dump>`.

### Importing MAP spectrometer data

MAP spectrometer data can be imported using the `sparrow import-map` command.
The MAP spectrometer data archive is expected to be available within this directory
at `Data/MAP-Irradiations`.

### Bulk metadata import

Metadata can be imported using the command `sparrow import-metadata`.
This currently expects a file `Data/WiscAr_metadata_v2.xlsx` within this repository.

## Todo

- [ ] Implement Noblesse spectrometer import
- [ ] Implement importer for PyChron interpreted ages
- [ ] Switch to number-based versioning instead of including the Sparrow submodule
