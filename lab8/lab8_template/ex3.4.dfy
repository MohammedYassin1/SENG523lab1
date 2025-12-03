lemma Ex4(x: int)
ensures 7 * x + 5 < (x + 3) * (x + 4)
{
    calc {
        (x + 3) * (x + 4);
        == {
            assert (x + 3) * (x + 4) == x * (x + 4) + 3 * (x + 4);
        }
        x * (x + 4) + 3 * (x + 4);
        == {
            assert x * (x + 4) == x * x + 4 * x;
            assert 3 * (x + 4) == 3 * x + 12;
        }
        (x * x + 4 * x) + (3 * x + 12);
        == {
            assert (x * x + 4 * x) + (3 * x + 12) == x * x + 7 * x + 12;
        }
        x * x + 7 * x + 12;
    }
}