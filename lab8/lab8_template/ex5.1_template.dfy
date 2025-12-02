method Mul(a: int, b: int) returns (prod: int)
  requires b >= 0
{
  var i := 0;
  prod := 0;
  while i < b
    // TODO: add invariant(s)
    // TODO: add decreases clause 
  {
    prod := prod + a;
    i := i + 1;
  }

  assert prod == a * b;
}
