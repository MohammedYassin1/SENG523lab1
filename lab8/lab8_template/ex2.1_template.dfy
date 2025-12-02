function SumTo(n: nat): nat
  // TODO: add decrease clause
  // TODO: add method contract
{
  if n == 0 then
    0
  else
    n + SumTo(n - 1)
}
