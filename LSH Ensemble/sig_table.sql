-- delete from public.sig_table;

CREATE OR replace FUNCTION min_hash_array(bigint[]) RETURNS bigint[]
	AS '/Library/PostgreSQL/12/include/postgresql/server/funcs', 'min_hash_array_new'
	LANGUAGE c;

CREATE OR REPLACE FUNCTION formatJSON(hashVector bigint[], keyNum integer) RETURNS jsonb AS $$
DECLARE
	arrayString varchar;
	domainRecord jsonb;
BEGIN
	arrayString = concat('{', array_to_string(hashVector, ','), '}');
	domainRecord = json_build_object('hashKey', arrayString, 'key', keyNum);
	RETURN domainRecord;
END;
$$ LANGUAGE plpgsql;

-- kNum is the number of hash functions in a band
-- lNum is the number of bands
CREATE OR REPLACE function insertHash(kNum integer, lNum integer) Returns void AS $$
DECLARE
	key1 integer;
	key2 integer;
	key3 integer;
	key4 integer;
	sig_vector1 bigint[];
	sig_vector2 bigint[];
	sig_vector3 bigint[];
	sig_vector4 bigint[];
	rv RECORD;
BEGIN
	FOR i IN 0..(lNum-1) LOOP
		FOR rv in
			execute 'SELECT * from public.sig_table t0 where t0."hashIdx" > $1 AND t0."hashIdx" <= $2' using i*kNum, (i+1)*kNum
		LOOP
			key1 = (rv."A"->>'key')::integer;
			key2 = (rv."B"->>'key')::integer;
			key3 = (rv."C"->>'key')::integer;
			key4 = (rv."D"->>'key')::integer;
			sig_vector1 = array_append(sig_vector1, (rv."A"->>'hv')::bigint);
			sig_vector2 = array_append(sig_vector2, (rv."B"->>'hv')::bigint);
			sig_vector3 = array_append(sig_vector3, (rv."C"->>'hv')::bigint);
			sig_vector4 = array_append(sig_vector4, (rv."D"->>'hv')::bigint);
		END LOOP;
		
		execute 'INSERT INTO public.hash_table VALUES ($1, $2, $3, $4, $5)'
			using i+1, formatJSON(min_hash_array(sig_vector1), key1),
			formatJSON(min_hash_array(sig_vector2), key2),
			formatJSON(min_hash_array(sig_vector3), key3),
			formatJSON(min_hash_array(sig_vector4), key4);
		
		sig_vector1 = '{}';
		sig_vector2 = '{}';
		sig_vector3 = '{}';
		sig_vector4 = '{}';
	END LOOP;
END;
$$ LANGUAGE plpgsql;

-- select min_hash_array('{12335, 212390, 38897123, 412309, 512397}');

-- select * from public.sig_table t0;
delete from public.hash_table;
select insertHash(4, 32);
-- select (t0."A"->>'sig')::bigint[] from public.sig_table t0;