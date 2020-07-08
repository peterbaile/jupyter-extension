-- delete from public.sig_table;

-- INSERT INTO public.sig_table VALUES ('{}', '{}', '1');
-- INSERT INTO public.sig_table VALUES ('{}', '{}', '2');

-- UPDATE public.sig_table SET "A" = array_append("A", '3') where "band" = 1;

CREATE OR REPLACE FUNCTION min_hash_array(ls bigint[]) RETURNS bigint AS $$
DECLARE
  s bigint := 999999999999999;
  x bigint;
  hv bigint;
BEGIN
  FOREACH x IN ARRAY ls
  LOOP
  	hv := min_hash(x);
  	IF s > hv THEN
		s := hv;
    END IF;
  END LOOP;
  RETURN s;
END;
$$ LANGUAGE plpgsql;

select * from public.sig_table;