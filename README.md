### Install Backend Server Extension
- `sudo python setup.py install`
- `jupyter serverextension enable --py juneau_extension`

### Install Client Notebook Extension
- `cd juneau_extension`
- `jupyter nbextension install default_cell/ --user`
- `jupyter nbextension enable default_cell/main --user`

### Invoke the Jupyter Server Extension
- `sh api.sh`
- GET request: `curl http://localhost:8888/juneau-2`
- Concurrent `GET` requests: `curl http://localhost:8888/juneau-2 & curl http://localhost:8888/juneau-2`