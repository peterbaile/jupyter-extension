CREATE OR replace FUNCTION min_hash(bigint, integer) RETURNS bigint
  	AS '/Library/PostgreSQL/12/include/postgresql/server/funcs', 'min_hash'
  	LANGUAGE c STRICT;

CREATE OR REPLACE function insert_sig(band_num integer, hash_num bigint) Returns void AS $$
DECLARE
	min_hv bigint;
BEGIN
 	select MIN(min_hash(t0."A", hash_num)) into min_hv from public.df0 t0;
	UPDATE public.sig_table SET "A" = array_append("A", hash_num) where "band" = band_num; 
END;
$$ LANGUAGE plpgsql;

call insert_sig(1, 1);
call insert_sig(1, 2);
call insert_sig(2, 3);
call insert_sig(2, 4);