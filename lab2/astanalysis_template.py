import sys
import ast

def main():
    if len(sys.argv) == 3 and sys.argv[1] == "unused":
        return do_unused(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "returns":
        return do_returns(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "constant":
        return do_constant(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "secret":
        return do_secret(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "taint":
        return do_taint(sys.argv[2])
    else:
        print("Usage: python astanalysis.py <cmd> <file>")
        return -1
    
# Exercise 1
def do_unused(fname):
    print("UNUSED not implemented")
    return -1

# Exercise 2
def do_returns(fname):
    print("RETURNS not implemented")
    return -1

# Exercise 3
def do_constant(fname):
    print("CONSTANT not implemented")
    return -1

# Exercise 4
def do_secret(fname):
    print("SECRET not implemented")
    return -1

# Exercise 5
def do_taint(fname):
    print("TAINT not implemented")
    return -1


if __name__ == "__main__":
    main()
