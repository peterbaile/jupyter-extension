-- delete from public.hash_table;

-- insert into public.json_table values ('{"sig": "{1, 2, 3}", "key": 1, "size": 4, "s": "abcd"}'::jsonb);

-- select '{"size": (t0."A"->>"size")::integer + 1, "key": t0."A"->>"key"}'::jsonb from public.json_table t0;

-- select min_hash_char((t0."A"->>'s')::varchar, 1) from public.json_table t0;

-- select (t0."A"->> 'hashKey')::bigint[] from public.hash_table t0;

select * from public.hash_table;