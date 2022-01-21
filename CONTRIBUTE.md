# Contributing to the UCO MIME taxonomy


## Environment setup

1. For formatting purposes, have available a Java version capable of running [RDF Toolkit](https://github.com/edmcouncil/rdf-toolkit), the tool [used](https://github.com/casework/CASE/blob/master/NORMALIZING.md) by the CASE community for Turtle content style normalization.
2. Have Python 3, version 3.7 or later, installed.
3. Have `make` available.


## Running build and unit tests

1. `git-clone` this repository and `cd` into its top directory.
2. (Optional) Run `make`.  This will re-build `mime.ttl`.  `git status` will show any changes since the last build.
3. Run `make check` to confirm unit tests pass against the built `mime.ttl`.
