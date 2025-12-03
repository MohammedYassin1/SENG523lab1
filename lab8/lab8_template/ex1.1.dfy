function Sign(x: int): int
  //TODO: add method contract
  ensures (x > 0) ==> Sign(x) == 1
  ensures (x == 0) ==> Sign(x) == 0
  ensures (x < 0) ==> Sign(x) == -1
{
  // TODO: add method implementation
  if x < 0 then
    -1
  else if x > 0 then
    1
  else
    0
}


method Main(args: seq<string>)
{
  var realArgs := args;
  if |realArgs| > 0 && realArgs[0] == "dotnet" {
    realArgs := realArgs[1..];
  }

  if |realArgs| < 1 {
    print "Usage: ex1.1 <x>\n";
    return;
  }

  var x := ParseInt(realArgs[0]);
  var r := Sign(x);
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
