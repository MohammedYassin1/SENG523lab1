function Dist(x: int, y: int): int
  // TODO: add method contract
  ensures Dist(x, y) >= 0
  ensures x - y >= 0 ==> Dist(x, y) == x - y
  ensures x - y < 0  ==> Dist(x, y) == y - x
  ensures Dist(x, y) == if x <= y then y - x else x - y
{
  // TODO: add method implementation
  if x <= y then
    y - x
  else
    x - y
}


method Main(args: seq<string>)
{
  var realArgs := args;
  if |realArgs| > 0 && realArgs[0] == "dotnet" {
    realArgs := realArgs[1..];
  }

  if |realArgs| < 2 {
    print "Usage: ex1.1_solution <x> <y>\n";
    return;
  }

  var x := ParseInt(realArgs[0]);
  var y := ParseInt(realArgs[1]);
  var r := Dist(x, y);
  print r, "\n";
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
