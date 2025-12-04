lemma Ex3(x: int, y: int)
ensures 2 * (x + 4 * y + 7) - 10 == 2 * x + 8 * y + 4
{
    calc {
        2 * (x + 4 * y + 7) - 10;
        == {
            assert 2 * (x + 4 * y + 7) - 10 == 2 * x + 8 * y + 14 - 10;
        }
        2 * x + 8 * y + 14 - 10;
        == {
            assert 2 * x + 8 * y + 14 - 10 == 2 * x + 8 * y + 4;
        }
        2 * x + 8 * y + 4;
    }
}