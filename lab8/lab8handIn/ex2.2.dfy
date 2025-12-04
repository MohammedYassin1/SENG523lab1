function Fact(n: nat): nat
  // TODO: add decreases clause
  decreases n
  // TODO: add method contract
  ensures Fact(n) == if n == 0 then 1 else n * Fact(n - 1)
{
  if n == 0 then
    1
  else
    n * Fact(n - 1)
}
