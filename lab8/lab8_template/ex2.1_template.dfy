function SumTo(n: nat): nat
  // TODO: add decrease clause
  decreases n
  // TODO: add method contract
  ensures n >= 0
  ensures SumTo(n) == n * (n + 1) / 2
{
  if n == 0 then
    0
  else
    n + SumTo(n - 1)
}
