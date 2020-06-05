### Install Backend Server Extension
- `sudo python setup.py install`
- `jupyter serverextension enable --py juneau_extension`

### Install Client Notebook Extension
- `cd juneau_extension`
- `jupyter nbextension install default_cell/ --user`
- `jupyter nbextension enable default_cell/main --user`