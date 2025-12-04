lemma Ex4(x: int)
ensures 7 * x + 5 < (x + 3) * (x + 4)
{
    calc {
        7 * x + 5; 
        < {
            assert 7 * x + 5 < x * x + 7 * x + 12;
        }
        x * x + 7 * x + 12;
        == {
            assert x * x + 7 * x + 12 == x * (x + 4) + 3 * (x + 4);
        }
        x * (x + 4) + 3 * (x + 4);
        == {
            assert x * (x + 4) + 3 * (x + 4) == (x + 3) * (x + 4);
        }
        (x + 3) * (x + 4);
    }
}