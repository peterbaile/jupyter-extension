from sqlalchemy import create_engine
import juneau_extension.config as cfg


def jaccard_similarity(table_a, table_b):
    sql_name = cfg.sql_name
    sql_password = cfg.sql_password
    sql_dbname = cfg.sql_dbname
    sql_schema_name = cfg.sql_schema_name

    conn_string = f"postgresql://{sql_name}:{sql_password}@localhost/{sql_dbname}"

    # Step 1: find the union of the two tables (union automatically selects distinct rows)
    union_string = f"SELECT * FROM {sql_schema_name}.{table_a} UNION SELECT * FROM {sql_schema_name}.{table_b}"

    # step 2: find the intersection of the two tables (INTERSECT automatically selects distinct rows)
    intersect_string = f"SELECT * FROM {sql_schema_name}.{table_a} INTERSECT SELECT * FROM {sql_schema_name}.{table_b}"

    # step 3: get the number of rows for the union & intersection respectively
    count_union_string = f'SELECT COUNT(*) AS "UNION_COUNT", 1 AS "idx" FROM ({union_string}) AS sub'
    count_intersect_string = f'SELECT COUNT(*) AS "INTER_COUNT", 1 AS "idx" FROM ({intersect_string}) AS sub2'

    # step 4: compute the jaccard similarity by joining the two tables and perform division
    jaccard_string = 'SELECT CAST("INTER_COUNT" AS float)/CAST ("UNION_COUNT" AS float) AS jaccard_sim FROM '
    jaccard_string += f'({count_intersect_string}) t1 INNER JOIN ({count_union_string}) t2 ON t2."idx" = t1."idx";'

    engine = create_engine(conn_string)

    with engine.connect() as connection:
        result = connection.execute(jaccard_string)
        for ls in result:
            return ls[0]


sim = jaccard_similarity('df1', 'df2')
print(sim)
