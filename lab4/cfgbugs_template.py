import sys

def main():
    if len(sys.argv) == 3 and sys.argv[1] == "stores":
        return do_stores(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "returns":
        return do_returns(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "taints":
        return do_taints(sys.argv[2])
    else:
        print("Usage: python cfgbugs.py <cmd> <file>")
        return -1
    
# Exercise 1
def do_stores(fname):
    print("STORES not implemented")
    return -1

# Exercise 2
def do_returns(fname):
    print("RETURNS not implemented")
    return -1

# Exercise 3
def do_taints(fname):
    print("TAINTS not implemented")
    return -1


if __name__ == "__main__":
    main()
