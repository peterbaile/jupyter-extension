#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include "fnv/fnv.h"

int HashValueSize = 4;
// u_int32_t INT_32_MAX = 2147483647;

/**
 * seed: the seed value
 * hashFuncIdx is the index of minwise hash function being used
 */
u_int64_t minHash(u_int32_t seed, char *s, int strLength, int hashFuncIdx) {
  srand(seed);

  unsigned char b1[HashValueSize];
  unsigned char b2[HashValueSize];

  for (int i = 0; i < HashValueSize; i++) {
    b1[i] = rand();
  }

  for (int i = 0; i < HashValueSize; i++) {
    b2[i] = rand();
  }

  Fnv32_t hv1;
  hv1 = fnv_32a_buf(b1, HashValueSize, FNV1_32A_INIT);
  hv1 = fnv_32a_buf(s, strLength, hv1);

  Fnv32_t hv2;
  hv2 = fnv_32a_buf(b2, HashValueSize, FNV1_32A_INIT);
  hv2 = fnv_32a_buf(s, strLength, hv2);

  return (u_int64_t) (hv1 + hashFuncIdx * hv2);
}

// int main() {
//   char s[] = "p";
//   printf("%" PRId64 "\n", minHash(1, s, 1, 1));
//   return 0;
// }