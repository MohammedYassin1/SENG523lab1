function SumFromTo(a: int, b: int): int
  // TODO: add the decreases clause
  decreases b - a + 1
  // TODO: add the method contract
  requires a <= b
  ensures SumFromTo(a, b) == (b * (b + 1) / 2) - ((a - 1) * a / 2)
{
  if a == b then
    a
  else
    a + SumFromTo(a + 1, b)
}
