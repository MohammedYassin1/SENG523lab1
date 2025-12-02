function Bump(n: int): int
{
  if n <= 0 then 1 else Bump(n - 1) + 1
}


lemma {:induction false} BumpGreater(n: int)
  ensures Bump(n) > n
{
  // TODO: add proof of lemma
}


method ExampleLemmaUse(a: int) {
    // TODO: state lemma appropriately to enable
    // Dafny to prove the final assertion
    var b := Bump(a);
    var c := Bump(b);
    assert 2 <= c - a;
}


method Main(args: seq<string>)
{
  var realArgs := args;
  if |realArgs| > 0 && realArgs[0] == "dotnet" {
    realArgs := realArgs[1..];
  }

  if |realArgs| < 1 {
    print "Usage: ex1.1_solution <x>\n";
    return;
  }

  var x := ParseInt(realArgs[0]);
  var r := Bump(x);
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
