CREATE OR replace FUNCTION min_hash_char(character varying, integer, integer) RETURNS bigint
  	AS '/Library/PostgreSQL/12/include/postgresql/server/funcs', 'min_hash_char'
  	LANGUAGE c STRICT;

CREATE OR REPLACE function insert_sig(numHash integer) Returns void AS $$
DECLARE
 	min_hv1 bigint;
	min_hv2 bigint;
	min_hv3 bigint;
	min_hv4 bigint;

	jMinHash1 jsonb;
	jMinHash2 jsonb;
	jMinHash3 jsonb;
	jMinHash4 jsonb;
BEGIN
	FOR i IN 1..numHash LOOP
		execute 'select MIN(min_hash_char(t0."A", LENGTH(t0."A"), $1)) from public.df0 t0' into min_hv1 using i;
		execute 'select MIN(min_hash_char(t0."B", LENGTH(t0."A"), $1)) from public.df0 t0' into min_hv2 using i;
 		execute 'select MIN(min_hash_char(t0."C", LENGTH(t0."C"), $1)) from public.df0 t0' into min_hv3 using i;
		execute 'select MIN(min_hash_char(t0."D", LENGTH(t0."D"), $1)) from public.df0 t0' into min_hv4 using i;
		
		jMinHash1 = json_build_object('hv', min_hv1, 'key', 1);
		jMinHash2 = json_build_object('hv', min_hv2, 'key', 2);
		jMinHash3 = json_build_object('hv', min_hv3, 'key', 3);
		jMinHash4 = json_build_object('hv', min_hv4, 'key', 4);
		execute 'insert into public.sig_table values ($1, $2, $3, $4, $5)' using i, jMinHash1, jMinHash2, jMinHash3, jMinHash4;
	END LOOP;
END;
$$ LANGUAGE plpgsql;

select insert_sig(128);