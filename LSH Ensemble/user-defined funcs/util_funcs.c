#include <string.h>
#include <stdio.h>

unsigned char * convert_to_byte_array(u_int64_t num) {
  static unsigned char buf[8];
  unsigned char c = 0;

  int idx = 0;

  for (int i = 0; i < 8; i++) {
    buf[i] = 0;
  }

  while (num > 0) {
    for (int i = 0; (i < 8) && (num > 0); i++) {
      c = ((num % 2) << i) + c;
      num = num / 2;
    }
    buf[idx] = c;
    idx ++;
    c = 0;
  }

  return buf;
}

unsigned char * hash_sig(u_int64_t sig[], int sig_len) {
  int hashValueSize = 4;
  unsigned char s[hashValueSize * sig_len];

  for (int i = 0; i < sig_len; i++) {
    unsigned char *buf;
    buf = convert_to_byte_array(sig[i]);

    int s_idx = i * hashValueSize;

    for (int j = 0; j < hashValueSize; j++) {
      s[s_idx] = buf[j];
      s_idx ++;
    }
  }

  return s;
}

int main() {
  // u_int64_t sig[] = {12335, 212390, 38897123, 412309, 512397};
  u_int64_t sig[] = {1098775865};

  unsigned char *p = hash_sig(sig, 1);

  for (int i = 0; i < 4; i++) {
      printf("%u ", *(p + i));
   }

  return 0;
}