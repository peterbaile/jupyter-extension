-- delete from public.sig_table;

CREATE OR replace FUNCTION min_hash_array(bigint[]) RETURNS bigint[]
	AS '/Library/PostgreSQL/12/include/postgresql/server/funcs', 'min_hash_array_new'
	LANGUAGE c;

-- arguments are k, l, x, q, t
-- returns [optk, optL]
CREATE OR replace FUNCTION computeOptKL(integer, integer, integer, integer, float8) RETURNS bigint[]
	AS '/Library/PostgreSQL/12/include/postgresql/server/funcs', 'computeOptimalKL'
	LANGUAGE c;

-- lNum is the number of bands
CREATE OR REPLACE function insertHashQuery(lNum integer) Returns void AS $$
DECLARE
	optK integer;
	optL integer;
	optValues integer[];
	sig_vector1 bigint[];
	rv RECORD;
BEGIN
	execute 'SELECT t."optK" from public.optimalkl_table t WHERE t."k"=$1 AND t."l"=$2 AND t."x"=$3 AND t."q"=$4 AND t."t"=$5'
		into optK using 4, 32, 4, 4, 0.9;
	IF optK is null THEN
		optValues = computeOptKL(4, 32, 4, 4, 0.9);
		optK = optValues[1]; -- postgres array are 1-indexed
		optL = optValues[2];
		execute 'INSERT INTO public.optimalkl_table VALUES ($1, $2, $3, $4, $5, $6, $7)' using 4, 32, 4, 4, 0.9, optK, optL;
	END IF;
	
	FOR i IN 0..(lNum-1) LOOP
		FOR rv in
			execute 'SELECT * from public.sig_query_table t0 where t0."hashIdx" > $1 AND t0."hashIdx" <= $2' using i*optK, (i+1)*optK
		LOOP
			sig_vector1 = array_append(sig_vector1, rv."A");
		END LOOP;
		
		execute 'INSERT INTO public.hash_query_table VALUES ($1, $2)'
			using i+1, min_hash_array(sig_vector1);
		
		sig_vector1 = '{}';
	END LOOP;
END;
$$ LANGUAGE plpgsql;

delete from public.hash_query_table;
select insertHashQuery(32);
select * from public.hash_query_table t0;