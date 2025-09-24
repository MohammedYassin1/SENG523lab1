import sys
import ast
import zss

def compare(n1,n2):
    # get all the children
    children1 = list(ast.iter_child_nodes(n1))
    children2 = list(ast.iter_child_nodes(n2))

    if type(n1) == type(n2):
        if len(children1) == len(children2):
            for i in range(len(children1)):
                equal = compare(children1[i], children2[i])

                if not equal:
                    return False
            return True
        else:
            return False
    else:
        return False

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
    with open(fname1, "r") as f:
        code = f.read()

    with open(fname2, "r") as f:
        code2 = f.read()
    
    tree1 = ast.parse(code)
    tree2 = ast.parse(code2)

    print(ast.dump(tree1, indent=4))
    print(ast.dump(tree2, indent=4))

    if compare(tree1, tree2):
        print("The programs are identical")
    else:
        print ("The programs are not identical")

#    print("WHOPS! 'cmd' command not implemented!")
#    return -1

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