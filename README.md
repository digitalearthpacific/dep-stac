# DEP STAC

This repo contains configurations for a container to manage
our STAC documents.

## Adding a product

### Create a collection

Create the collection in the `dep_collections` folder by copying one of the existing products.
Update all the fields as appropriate, ensureing it's accurately reflecting the data being
produced.

### Add an entry for production/staging

Add the new collection to the [`create_collections.py`](create_collections.py) file,
including which of `production/staging` catalogs to include it in.

### Run the collection creation

Run the command `make create_collections` or `python create_collections.py` to
set up the collections JSON documents.

### Create a pull request

Create a pull request, get it reviewed. Once merged, run the appropriate Argo workflow.

## Adding documents to databse

### Collections

```bash
For all the files in the collections folder, load them into the database
ls | xargs -L 1 -d '\n' \
  pypgstac load collections --method upsert
```

### Items

```bash
python ./get_insert_items.py \
  --bucket=my-bucket \
  --prefix=path/to/collection
```
