rm funcs.o
rm funcs.so
rm hash_32a.o

cc -c -I/Library/PostgreSQL/12/include/postgresql/server/ -Ifnv/ funcs.c fnv/hash_32a.c
cc -bundle -flat_namespace -undefined suppress -o funcs.so funcs.o hash_32a.o