#include <float.h>
#include <string.h>
#include "probability.h"

void optimalKL(int k, int l, int x, int q, double t, int *optK, int *optL) {
  double minError = DBL_MAX;
  double integrationPrecision = 0.01;

  for (int i = 1; i <= l; i++) {
    for (int j = 1; j <= k; j++) {
      double currFp = probFalsePositive(x, q, l, k, t, integrationPrecision);
      double currFn = probFalseNegative(x, q, l, k, t, integrationPrecision);
      double currErr = currFp + currFn;

      if (minError > currErr) {
        minError = currErr;
        *optK = k;
        *optL = l;
      }
    }
  }
}

void query(u_int64_t hashRow[], u_int64_t hashKey[]) {
  
}