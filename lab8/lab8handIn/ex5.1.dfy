method Mul(a: int, b: int) returns (prod: int)
  requires b >= 0
{
  var i := 0;
  prod := 0;
  while i < b
    // TODO: add invariant(s)
    invariant prod == a * i
    invariant 0 <= i <= b
    // TODO: add decreases clause 
    decreases b - i
  {
    prod := prod + a;
    i := i + 1;
  }

  assert prod == a * b;
}
