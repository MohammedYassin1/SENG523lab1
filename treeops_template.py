import sys
import ast
import zss

def main():
    if len(sys.argv) == 4 and sys.argv[1] == "cmp":
        return do_cmp(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == "dst":
        return do_dst(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == "run":
        return do_run(sys.argv[2])
    else:
        print("Usage: python treeops.py <cmd> <file 1> <optional file 2>")
        return -1

# Provide the solution to Exercise 2 by implementing the function below
def do_cmp(fname1, fname2):
    print("WHOPS! 'cmd' command not implemented!")
    return -1

# Provide the solution to Exercise 3 by implementing the function below
def do_dst(fname1, fname2):
    print("WHOPS! 'dst' command not implemented!")
    return -1

# Provide the solution to Exercise 4 by implementing the function below
def do_run(fname):
    print("WHOPS! 'run' command not implemented!")
    return -1


if __name__ == "__main__":
    main()