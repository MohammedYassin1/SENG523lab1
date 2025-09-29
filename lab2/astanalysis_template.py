import sys
import ast


class ConstantConditionVisitor(ast.NodeVisitor):
    constant_condition = False

    def visit_If(self, node):
        self.constant_check(node.test)
        if self.constant_condition == True:
            print("Conditional statement with constant condition detected")
            self.constant_condition = False
        else:
            print("no output")

        self.generic_visit(node)
    
    def visit_IfExp(self, node):
        self.constant_check(node.test)
        if self.constant_condition == True:
            print("Conditional statement with constant condition detected")
            self.constant_condition = False
        else:
            print("no output")
        self.generic_visit(node)

    def constant_check(self, node):
        if isinstance(node, ast.Constant):
            self.constant_condition = True
        elif isinstance(node, ast.Compare):
            left = isinstance(node.left, ast.Constant)
            rights = False
            for comp in node.comparators:
                if isinstance(comp, ast.Constant):
                    rights = True
                else:
                    rights = False
                    break
            if left and rights:
                self.constant_condition = True
            

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
    ast.parse(open(fname).read())
    
    return -1

# Exercise 2
def do_returns(fname):
    print("RETURNS not implemented")
    return -1

# Exercise 3
def do_constant(fname):
    with open(fname) as f:
        tree = ast.parse(f.read(), filename=fname)
    visitor = ConstantConditionVisitor()
    visitor.visit(tree)
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
