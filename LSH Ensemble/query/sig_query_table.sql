CREATE OR replace FUNCTION min_hash_char(character varying, integer, integer) RETURNS bigint
  	AS '/Library/PostgreSQL/12/include/postgresql/server/funcs', 'min_hash_char'
  	LANGUAGE c STRICT;

CREATE OR REPLACE function insert_sig_query(numHash integer) Returns void AS $$
DECLARE
 	min_hv1 bigint;
BEGIN
	FOR i IN 1..numHash LOOP
		execute 'select MIN(min_hash_char(t0."A", LENGTH(t0."A"), $1)) from public.query_table t0' into min_hv1 using i;
		execute 'insert into public.sig_query_table values ($1, $2)' using i, min_hv1;
	END LOOP;
END;
$$ LANGUAGE plpgsql;

delete from public.sig_query_table;
select insert_sig_query(128);
select * from public.sig_query_table;