function Pow2(k: nat): nat
  // TODO: add the decreases clause
  // TODO: add the method contract
{
  if k == 0 then
    1
  else
    2 * Pow2(k - 1)
}
