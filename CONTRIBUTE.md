## Refreshing the taxonomy

The following steps are taken to refresh the taxonomy's individuals:

```bash
git clone https://github.com/ucoProject/UCO-Taxonomy-MIME.git
pushd UCO-Taxonomy-MIME
  git checkout -b refresh-$(date -u +%Y-%m-%d)
  make
  git diff  # Have a view of what changed
  make check  # If an error occurs, please file a Github Issue.
  git commit  # A typical commit message could be "Regenerate Make-managed files"
  git push
  # And now is a good time to file a pull request,
  # so the maintainers can know to issue a release.
popd #UCO-Taxonomy-MIME
# The UCO-Taxonomy-MIME folder is no longer needed.
```


## Supplementing the taxonomy

The taxonomy is built from two sources:

1. An RDF render of the [IANA Media Types XML feed](https://www.iana.org/assignments/media-types/media-types.xml).
2. A set of hard-coded taxons and relationships, in [`taxonomy/mime/mime-base.ttl`](taxonomy/mime/mime-base.ttl).

Non-automated revision to the taxonomy, such as incrementing the stamped version or addition of a taxon or taxon relationship, should be done as modifications to `mime-base.ttl`.  Then, `make` should be run to regenerate the monolithic `mime.ttl`.  (Please run the steps in the "Refreshing the taxonomy" section above and commit results before making manual modifications, in case new IANA Media Types have been posted since the last build.  This isolates impacts of manual revisions.)
