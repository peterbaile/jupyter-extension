#include <stdio.h>
#include <math.h>
#include <float.h>

long double falsePositive(long x, long q, long l, long k, double t)
{
  return 1.0 - pow(1.0 - pow(t / (1.0 + (long double)x / (long double)q - t), (long double)k), (long double)l);
}

long double falseNegative(long x, long q, long l, long k, double t)
{
  return 1.0 - (1.0 - pow(1.0 - pow(t / (1.0 + (long double)x / (long double)q - t), (long double)k), (long double)l));
}

long double integralFP(long x, long q, long l, long k, double a, double b, double precision)
{
  long double area = 0.0;

  for (double i = a; i < b; i += precision)
  {
    area += falsePositive(x, q, l, k, i + 0.5 * precision) * precision;
  }

  return area;
}

long double integralFN(long x, long q, long l, long k, double a, double b, double precision)
{
  long double area = 0.0;

  for (double i = a; i < b; i += precision)
  {
    area += falseNegative(x, q, l, k, i + 0.5 * precision) * precision;
  }

  return area;
}

long double probFalseNegative(long x, long q, long l, long k, double t, double precision)
{
  long double xq = (long double)x / (long double)q;

  if (xq >= 1.0)
  {
    return integralFN(x, q, l, k, t, 1.0, precision);
  }

  if (xq >= t)
  {
    return integralFN(x, q, l, k, t, xq, precision);
  }
  else
  {
    return 0.0;
  }
}

long double probFalsePositive(long x, long q, long l, long k, double t, double precision)
{
  long double xq = (long double)x / (long double)q;

  if (xq >= 1.0 || xq >= t)
  {
    return integralFP(x, q, l, k, 0.0, t, precision);
  }
  else
  {
    return integralFP(x, q, l, k, 0.0, xq, precision);
  }
}

// k is the number of hash functions in each band
// l is the number of bands
// x is the domain size
// q is the query size
// t is the threshold value
// optK and optL are the pointers to store the optimal k and l values
void optimalKL(long k, long l, long x, long q, double t, long *optK, long *optL) {
  long double minError = DBL_MAX;
  double integrationPrecision = 0.01;

  for (long i = 1; i <= l; i++) {
    for (long j = 1; j <= k; j++) {
      long double currFp = probFalsePositive(x, q, i, j, t, integrationPrecision);
      long double currFn = probFalseNegative(x, q, i, j, t, integrationPrecision);
      long double currErr = currFp + currFn;

      if (minError > currErr) {
        // printf("%Lf\n", currErr);
        // printf("k value is %d ", i);
        // printf("j value is %d\n", j);
        minError = currErr;
        *optK = i;
        *optL = j;
      }
    }
  }
}

// int main()
// {
//   double precision = 0.01;
//   printf("%f\n", probFalsePositive(4, 4, 1, 1, 0.9, precision));
//   printf("%f\n", probFalseNegative(4, 4, 1, 1, 0.9, precision));
// }

// int main() {
//   long k = 5;
//   long l = 32;
//   long x = 1000000000000;
//   long q = 10000000;
//   double t = 0.6;

//   long optK = -1, optL = -1;

//   optimalKL(k, l, x, q, t, &optK, &optL);

//   printf("%ld\n", optK);
//   printf("%ld\n", optL);

//   return 0;
// }