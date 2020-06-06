import juneau_extension.config as cfg
from juneau_extension.jupyter import exec_code


code = f"""from sqlalchemy import create_engine
conn_string = f"postgresql://{cfg.sql_name}:{cfg.sql_password}@localhost/{cfg.sql_dbname}"
engine = create_engine(conn_string)
print("hello")
with engine.connect() as conn:
    result = conn.execute("select * from {cfg.sql_schema_name}.{cfg.sql_table_name}")
    for row in result:
        print(row)
    """

output, error = exec_code('56966', 'df', code)

print(output)
