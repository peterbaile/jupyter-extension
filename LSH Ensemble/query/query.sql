CREATE OR REPLACE FUNCTION checkHashKeys(hqKeys bigint[], hKeys bigint[], prefixSize integer, similarSet integer[], keyNum integer) RETURNS integer[] AS $$
BEGIN
	-- array is 1-indexed in PostgresSQL
	FOR i IN 1..prefixSize LOOP
		IF hqKeys[i] != hKeys[i] THEN
			RETURN similarSet;
		END IF;
	END LOOP;
	similarSet = array_append(similarSet, keyNum);
	return similarSet;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION queryTable() RETURNS bigint[] AS $$
DECLARE
	optK integer;
	optL integer;
	hashValueSize integer = 4;
	prefixSize integer;
	
	similarSet integer[];
	lIdx integer = 0;
	rv RECORD;
BEGIN
	execute 'SELECT t."optK", t."optL" from public.optimalkl_table t WHERE t."k"=$1 AND t."l"=$2 AND t."x"=$3 AND t."q"=$4 AND t."t"=$5'
		into optK, optL using 4, 32, 4, 4, 0.9;
	prefixSize = hashValueSize * optK;
	
	FOR rv in
		select hq."A" as "qd", h."A", h."B", h."C", h."D" from public.hash_table h JOIN public.hash_query_table hq ON h."bandIdx" = hq."bandIdx"
	LOOP
		similarSet = checkHashKeys(rv."qd", (rv."A"->>'hashKey')::bigint[], prefixSize, similarSet, (rv."A"->>'key')::integer);
		similarSet = checkHashKeys(rv."qd", (rv."B"->>'hashKey')::bigint[], prefixSize, similarSet, (rv."B"->>'key')::integer);
		similarSet = checkHashKeys(rv."qd", (rv."C"->>'hashKey')::bigint[], prefixSize, similarSet, (rv."C"->>'key')::integer);
		similarSet = checkHashKeys(rv."qd", (rv."D"->>'hashKey')::bigint[], prefixSize, similarSet, (rv."D"->>'key')::integer);
		lIdx = lIdx + 1;
		EXIT WHEN lIdx >= optL;
	END LOOP;
	RETURN similarSet;
END;
$$ LANGUAGE plpgsql;

select queryTable();