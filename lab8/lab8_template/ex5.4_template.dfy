method ReachN(n: int) returns (i: int)
  requires n >= 0
{
  i := 0;
  while i < n
    // TODO: add invariant(s)
    // TODO: add decreases clause
  {
    i := i + 1;
  }

  assert i == n;
}