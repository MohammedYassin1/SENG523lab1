method Max3(a: int, b: int, c: int) returns (m: int)
  // TODO: method contract
  ensures m == a || m == b || m == c
{
  // TODO: method implementation
  if a >= b && a >= c {
    return a;
  } else if b >= c && b >= a {
    return b;
  } else {
    return c;
  }
}

method Main(args: seq<string>)
{
  var rArgs := args;
  if |rArgs| > 0 && rArgs[0] == "dotnet" {
    rArgs := rArgs[1..];
  }

  if |rArgs| < 3 {
    print "Usage: max3 <a> <b> <c>\n";
    return;
  }

  var a := ParseInt(rArgs[0]);
  var b := ParseInt(rArgs[1]);
  var c := ParseInt(rArgs[2]);

  var m := Max3(a, b, c);
  print m, "\n";
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
