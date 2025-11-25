method Clamp(x: int, lo: int, hi: int) returns (r: int)
  // TODO: method contract
  requires lo <= hi
{
  // TODO: method implementation
  if x < lo {
    return lo;
  } else if x > hi {
    return hi;
  } else {
    return x;
  }
}

method Main(args: seq<string>)
{
  var rArgs := args;
  if |rArgs| > 0 && rArgs[0] == "dotnet" {
    rArgs := rArgs[1..];
  }

  if |rArgs| < 3 {
    print "Usage: clamp <x> <lo> <hi>\n";
    return;
  }

  var x := ParseInt(rArgs[0]);
  var lo := ParseInt(rArgs[1]);
  var hi := ParseInt(rArgs[2]);

  if lo > hi {
    print "Error: lo must be less than or equal to hi\n";
    return;
  }

  var r := Clamp(x, lo, hi);
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

