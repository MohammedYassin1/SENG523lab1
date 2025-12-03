function Pow2(k: nat): nat
  // TODO: add the decreases clause
  decreases k
  // TODO: add the method contract
  ensures Pow2(k) >= 1
  ensures k == 0 ==> Pow2(k) == 1
  ensures k > 0  ==> Pow2(k) == 2 * Pow2(k - 1)
  // ensures Pow2(k) == 1 << k
{
  if k == 0 then
    1
  else
    2 * Pow2(k - 1)
}
