function Fact(n: nat): nat
  // TODO: add decreases clause
  // TODO: add method contract
{
  if n == 0 then
    1
  else
    n * Fact(n - 1)
}
