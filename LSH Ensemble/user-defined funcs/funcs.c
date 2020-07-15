#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "fnv.h"
#include "utils/array.h"
#include "utils/lsyscache.h"
#include "util_funcs.h"
#include "minhash.h"
#include "probability.h"

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

PG_FUNCTION_INFO_V1(min_hash_char);
Datum min_hash_char(PG_FUNCTION_ARGS)
{
    VarChar *arg = (VarChar *)PG_GETARG_VARCHAR_P(0);
    u_int32_t length = PG_GETARG_UINT32(1);
    u_int32_t hashIdx = PG_GETARG_UINT32(2);

    char *str = (char *)VARDATA(arg);

    // return the hashed value
    PG_RETURN_UINT64(minHash(1, str, length, hashIdx));
}

PG_FUNCTION_INFO_V1(min_hash_array_new);
Datum
min_hash_array_new(PG_FUNCTION_ARGS)
{
    // Our arguments:
    ArrayType *vals;

    // The array element type:
    Oid valsType;

    // The array element type widths for our input array:
    int16 valsTypeWidth;

    // The array element type "is passed by value" flags (not really used):
    bool valsTypeByValue;

    // The array element type alignment codes (not really used):
    char valsTypeAlignmentCode;

    // The array contents, as PostgreSQL "Datum" objects:
    Datum *valsContent;

    // List of "is null" flags for the array contents:
    bool *valsNullFlags;

    // The size of the input array:
    int valsLength;

    if (PG_ARGISNULL(0))
        ereport(ERROR, (errmsg("Null arrays not accepted")));

    vals = PG_GETARG_ARRAYTYPE_P(0);

    if (ARR_NDIM(vals) == 0)
    {
        PG_RETURN_NULL();
    }
    if (ARR_NDIM(vals) > 1)
    {
        ereport(ERROR, (errmsg("One-dimesional arrays are required")));
    }

    // Determine the array element types.
    valsType = ARR_ELEMTYPE(vals);

    valsLength = (ARR_DIMS(vals))[0];

    get_typlenbyvalalign(valsType, &valsTypeWidth, &valsTypeByValue, &valsTypeAlignmentCode);

    // Extract the array contents (as Datum objects).
    deconstruct_array(vals, valsType, valsTypeWidth, valsTypeByValue, valsTypeAlignmentCode,
                      &valsContent, &valsNullFlags, &valsLength);
    
    if (valsLength == 0) PG_RETURN_NULL();

    // array to hold the hashed signature
    Datum* hs;

    int hashValueSize = 4;

    // valsLength = k (#hash functions in each band)
    int hs_length = hashValueSize * valsLength;

    hs = palloc(sizeof(Datum) * hs_length);

    for (int i = 0; i < valsLength; i++) {
        unsigned char *buf;
        buf = convert_to_byte_array(valsContent[i]);

        int s_idx = i * hashValueSize;

        for (int j = 0; j < hashValueSize; j++) {
            hs[s_idx] = buf[j];
            s_idx++;
        }
    }

    ArrayType* result_array;

    result_array = construct_array(hs, hs_length, valsType, valsTypeWidth, valsTypeByValue, valsTypeAlignmentCode);

    PG_RETURN_ARRAYTYPE_P(result_array);
}

PG_FUNCTION_INFO_V1(computeOptimalKL);
Datum computeOptimalKL(PG_FUNCTION_ARGS)
{
    long k = PG_GETARG_UINT32(0);
    long l = PG_GETARG_UINT32(1);
    long x = PG_GETARG_UINT32(2);
    long q = PG_GETARG_UINT32(3);
    double t = PG_GETARG_FLOAT8(4);

    long optK = -1, optL = -1;

    optimalKL(k, l, x, q, t, &optK, &optL);

    // Oid intType = PG_GETARG_OID(0);
    int16 valsTypeWidth;
    bool valsTypeByValue;
    char valsTypeAlignmentCode;
    get_typlenbyvalalign(20, &valsTypeWidth, &valsTypeByValue, &valsTypeAlignmentCode);

    // array to hold values for optK and optL
    Datum* values;
    int valuesSize = 2;
    values = palloc(sizeof(Datum) * valuesSize);
    values[0] = optK;
    values[1] = optL;

    ArrayType* result_array;

    result_array = construct_array(values, valuesSize, 20, valsTypeWidth, valsTypeByValue, valsTypeAlignmentCode);

    PG_RETURN_ARRAYTYPE_P(result_array);
}