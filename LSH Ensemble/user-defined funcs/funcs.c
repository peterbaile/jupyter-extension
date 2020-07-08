#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "fnv.h"

PG_MODULE_MAGIC;

// PG_FUNCTION_INFO_V1(add_one);
// Datum add_one(PG_FUNCTION_ARGS)
// {
//     int32 arg = PG_GETARG_INT32(0);

//     PG_RETURN_INT32(arg + 1);
// }

PG_FUNCTION_INFO_V1(min_hash);
Datum min_hash(PG_FUNCTION_ARGS)
{
    // num is the number in the raw table that needs to be hashed
    u_int32_t num = PG_GETARG_INT64(0);

    // hash_num specify the hash function to be used
    u_int32_t hash_num = PG_GETARG_UINT32(1);

    Fnv32_t hash_val;
    
    // apply FNV1a Hash function to the number
    hash_val = fnv_32a_buf(&num, sizeof(num), FNV1_32A_INIT);

    // return the hashed value
    PG_RETURN_UINT64(hash_val * hash_num);
}