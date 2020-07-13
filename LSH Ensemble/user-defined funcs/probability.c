#include <stdio.h>
#include <math.h>

double falsePositive(int x, int q, int l, int k, double t)
{
  return 1.0 - pow(1.0 - pow(t / (1.0 + (double)x / (double)q - t), (double)k), (double)l);
}

double falseNegative(int x, int q, int l, int k, double t)
{
  return 1.0 - (1.0 - pow(1.0 - pow(t / (1.0 + (double)x / (double)q - t), (double)k), (double)l));
}

double integralFP(int x, int q, int l, int k, double a, double b, double precision)
{
  double area;

  for (double i = a; i < b; i += precision)
  {
    area += falsePositive(x, q, l, k, i + 0.5 * precision) * precision;
  }

  return area;
}

double integralFN(int x, int q, int l, int k, double a, double b, double precision)
{
  double area;

  for (double i = a; i < b; i += precision)
  {
    area += falseNegative(x, q, l, k, i + 0.5 * precision) * precision;
  }

  return area;
}

double probFalseNegative(int x, int q, int l, int k, double t, double precision)
{
  double xq = (double)x / (double)q;

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

double probFalsePositive(int x, int q, int l, int k, double t, double precision)
{
  double xq = (double)x / (double)q;

  if (xq >= 1.0 || xq >= t)
  {
    return integralFP(x, q, l, k, 0.0, t, precision);
  }
  else
  {
    return integralFP(x, q, l, k, 0.0, xq, precision);
  }
}

int main()
{
  double precision = 0.01;
  printf("%f\n", probFalsePositive(4, 1, 3, 2, 0.9, precision));
  printf("%f\n", probFalseNegative(4, 1, 3, 2, 0.9, precision));
}