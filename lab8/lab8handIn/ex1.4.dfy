function Median3(a: int, b: int, c: int): int
  // TODO: add method contract
  ensures (a <= b && b <= c) || (c <= b && b <= a) ==> Median3(a, b, c) == b
  ensures (b <= a && a <= c) || (c <= a && a <= b) ==> Median3(a, b, c) == a
  ensures (a <= c && c <= b) || (b <= c && c <= a) ==> Median3(a, b, c) == c
{
  // TODO: add method implementation
  if (a <= b && b <= c) || (c <= b && b <= a) then
    b
  else if (b <= a && a <= c) || (c <= a && a <= b) then
    a
  else
    c
}


method Main(args: seq<string>)
{
  var realArgs := args;
  if |realArgs| > 0 && realArgs[0] == "dotnet" {
    realArgs := realArgs[1..];
  }

  if |realArgs| < 3 {
    print "Usage: ex1.4_solution <x> <y> <z>\n";
    return;
  }

  var x := ParseInt(realArgs[0]);
  var y := ParseInt(realArgs[1]);
  var z := ParseInt(realArgs[2]);
  var med := Median3(x, y, z);
  print med, "\n";
}


method ParseInt(s: string) returns (n: int)
{
  var i := 0;
  var sign := 1;
  n := 0;

  if |s| == 0 {
    return;
  }

  if s[0] == '-' {
    sign := -1;
    i := 1;
  } else if s[0] == '+' {
    i := 1;
  }

  while i < |s|
  {
    var c := s[i] as int;
    var d := c - ('0' as int);

    if d < 0 || d > 9 {
      n := 0;
      return;
    }

    n := n * 10 + d;
    i := i + 1;
  }

  n := sign * n;
}
