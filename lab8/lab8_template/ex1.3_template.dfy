function Min(a: int, b: int): int
  // TODO: add method contract
{
  // TODO: add method implementation
}

function Max(a: int, b: int): int
  // TODO: add method contract
{
  // TODO: add method implementation
}


method Main(args: seq<string>)
{
  var realArgs := args;
  if |realArgs| > 0 && realArgs[0] == "dotnet" {
    realArgs := realArgs[1..];
  }

  if |realArgs| < 2 {
    print "Usage: ex1.3 <x> <y>\n";
    return;
  }

  var x := ParseInt(realArgs[0]);
  var y := ParseInt(realArgs[1]);
  var min := Min(x, y);
  var max := Max(x, y);
  print "Min: ", min, "\n";
  print "Max: ", max, "\n";
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
