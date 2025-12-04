method ReachN(n: int) returns (i: int)
  requires n >= 0
{
  i := 0;
  while i < n
    // TODO: add invariant(s)
    invariant 0 <= i <= n
    // TODO: add decreases clause
    decreases n - i
  {
    i := i + 1;
  }

  assert i == n;
}