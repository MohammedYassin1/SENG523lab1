lemma Ex1(x: int)
ensures 3 * (2 * x - 5) + 4 == 6 * x - 11
{
    calc {
        3 * (2 * x - 5) + 4;
        == {
            assert 3 * (2 * x - 5) + 4 == 6 * x - 15 + 4;
        }
        6 * x - 15 + 4;
        == {
            assert 6 * x - 15 + 4 == 6 * x - 11;
        }
        6 * x - 11;
    }
}