import sys
import logging
from jupyter_client import find_connection_file
from jupyter_client import MultiKernelManager, BlockingKernelClient, KernelClient

import juneau_extension.config as cfg

logging.basicConfig(level=logging.INFO)
TIMEOUT = 60


def main(kid, var, pid):
    # load connection info and init communication
    cf = find_connection_file(kid)  # str(port))
    km = KernelClient(connection_file=cf)
    km.load_connection_file()
    km.start_channels()

    # Step 0: get all the inputs

    load_input_code = f"""
proc_id="{pid}"
var={var}
var_name="{var}"
sql_name = "{cfg.sql_name}"
sql_password = "{cfg.sql_password}"
sql_dbname = "{cfg.sql_dbname}"
sql_schema_name = "{cfg.sql_schema_name}"
sql_table_name = "{cfg.sql_table_name}"
json_file_name = "/Users/peterchan/Desktop/GitHub/jupyter-extension/juneau_extension/data_file.json"
    """

    # Step 1: access the table and convert it to JSON

    request_var_code = f"""
import numpy as np
import pandas as pd
import json

if type(var) is pd.DataFrame or type(var) is np.ndarray or type(var) is list:
    df_json_string = var.to_json(orient='split', index=False)
    df_ls = json.loads(df_json_string)['data']
    df_ls_copy = copy.deepcopy(df_ls)
    """

    # Step 2: define the functions used to write to the JSON file

    json_lock_code = """
def initialize():
    data = {
        "ownerID": "",
        "id123": "operating",
        "id124": "finish"
    }
    with open("./juneau_extension/data_file.json", "w") as file:
        json.dump(data, file, indent=4)


def acquire_lock(pid):
    with open(json_file_name, "r+") as file:
        try:
            data = json.load(file)
            if data["ownerID"]:
                return False
            else:
                file.seek(0)
                file.truncate()
                data['ownerID'] = pid
                json.dump(data, file, indent=4)
                return True
        except Exception:
            return False


def release_lock(pid):
    with open(json_file_name, "r+") as file:
        data = json.load(file)
        if data['ownerID'] == pid:
            file.seek(0)
            file.truncate()
            data['ownerID'] = ""
            json.dump(data, file, indent=4)


# input: id of the process
# remove from the file if the process is completed/ terminated/ timed out
def update_exec_status(status, pid):
    done = False
    while not done:
        success = acquire_lock(pid)
        if success:
            try:
                with open(json_file_name, "r+") as file:
                    data = json.load(file)
                    if not data['ownerID'] == pid:
                        continue
                    file.seek(0)
                    file.truncate()
                    data[pid] = status
                    json.dump(data, file, indent=4)
                release_lock(pid)
                done = True
            except Exception:
                continue
    return True
    """

    # Step 3: connect to SQL and insert the table

    insert_code = """
from sqlalchemy import create_engine

conn_string = f"postgresql://{sql_name}:{sql_password}@localhost/{sql_dbname}"
table_string = f"{sql_schema_name}.{sql_table_name}"

engine = create_engine(conn_string)
with engine.connect() as connection:
    insertion_string = f'CREATE TABLE {sql_schema_name}.{var_name} ("A" int, "B" int, "C" int, "D" int);'
    for ls in df_ls_copy:
        insertion_string += f"INSERT INTO {sql_schema_name}.{var_name} VALUES ({ls[0]}, {ls[1]}, {ls[2]}, {ls[3]});"

    connection.execute(insertion_string)
    update_exec_status("done", proc_id)
    """

    code = load_input_code + request_var_code + json_lock_code + insert_code

    km.execute(code, store_history=False)
    # km.stop_channels()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
