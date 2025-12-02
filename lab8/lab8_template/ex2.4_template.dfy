function SumFromTo(a: int, b: int): int
  // TODO: add the decreases clause
  // TODO: add the method contract
{
  if a == b then
    a
  else
    a + SumFromTo(a + 1, b)
}
