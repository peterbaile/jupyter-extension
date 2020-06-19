### Install Backend Server Extension
- `sudo python setup.py install`
- `jupyter serverextension enable --py juneau_extension`

### Install Client Notebook Extension
- `cd juneau_extension`
- `jupyter nbextension install default_cell/ --user`
- `jupyter nbextension enable default_cell/main --user`

### Improvements
|                    | Previous                                                             | Current                                                                                   |
|--------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Jaccard Similarity | load the tables from Postgres to Python and compare it col by col    | using SQL query directly                                                                  |
| Indexing Table     | use a file lock to make each request run in a sequential order       | store execution status in a JSON file, allowing table indexing to be performed in parallel|