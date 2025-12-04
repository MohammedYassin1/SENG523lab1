method SumEven(n: int) returns (sum: int)
  requires n >= 0
{
  var i := 0;
  sum := 0;

  while i < n
    // TODO: add invariant(s)
    invariant sum == i * (i - 1)
    invariant 0 <= i <= n
    // TODO: add decreases clause
    decreases n - i
  {
    sum := sum + 2 * i;
    i := i + 1;
  }

  assert sum == n * (n - 1);
}
