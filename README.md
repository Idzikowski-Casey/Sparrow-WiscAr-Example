# Sparrow Example Implementation (WiscAr db)

This is an implementation of sparrow for the WiscAr Lab. This can be used as an example for creating
customized frontend and backend plugins for individual lab's instances of sparrow.

Customization depends heavily on the environmental variables a lab defines in it's `sparrow-config.sh` and `sparrow-config.overrides.sh`. 


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

### Restoring from a database dump

The state of an existing Sparrow installation can be restored using the command
`sparrow db-import <your-database.pg-dump>`.
