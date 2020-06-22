### Install Backend Server Extension
- `sudo python setup.py install`
- `jupyter serverextension enable --py juneau_extension`

### Install Client Notebook Extension
- `cd juneau_extension`
- `jupyter nbextension install default_cell/ --user`
- `jupyter nbextension enable default_cell/main --user`

### Improvements
|                    | Previous                                                             | Current                                                                                   
|--------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------
| Jaccard Similarity | load the tables from Postgres to Python and compare it col by col    | using SQL query directly ([code](https://github.com/peterbaile/jupyter-extension/blob/master/juneau_extension/jaccard.py))
| Indexing Table     | use a file lock to make each request run in a sequential order       | store execution status in a JSON file, allowing table indexing to be performed in parallel

**Flow of Indexing Table**

Front End: `put` requests are sent from the frontend to the , with the `kernel_id` and the `var_name`

Backend End: the `put` function in the `handler.py` invokes the function `exec_ipython` that consists of two parts: 1)
start a subprocess 2) triggers a while loop that checks the JSON file and see if the subprocess is completed

