import sys
import logging
from jupyter_client import find_connection_file
from jupyter_client import MultiKernelManager, BlockingKernelClient, KernelClient

import juneau_extension.config as cfg

logging.basicConfig(level=logging.INFO)
TIMEOUT = 60


def main(kid, var):
    # load connection info and init communication
    cf = find_connection_file(kid)  # str(port))
    km = BlockingKernelClient(connection_file=cf)
    km.load_connection_file()
    km.start_channels()

    code = f"""from sqlalchemy import create_engine
conn_string = f"postgresql://{cfg.sql_name}:{cfg.sql_password}@localhost/{cfg.sql_dbname}"
engine = create_engine(conn_string)
with engine.connect() as conn:
    result = conn.execute("select * from {cfg.sql_schema_name}.{cfg.sql_table_name}")
    for row in result:
        print("hello")
        print(row)
    """

    km.execute_interactive(code, timeout=TIMEOUT)
    km.stop_channels()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
