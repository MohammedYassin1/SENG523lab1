import sys
import ast
import zss

class NodeVisitor(ast.NodeVisitor):

    len = 0

    vars = {}

    final_var = None
    
    def generic_visit(self, node):
        assign_eq(node, NodeVisitor.vars)
        if node.__class__.__name__ != "Load" and node.__class__.__name__ != "Store":
            NodeVisitor.len += 1
        super().generic_visit(node)

    @staticmethod
    def get_children(node):
        return list(ast.iter_child_nodes(node))

    @staticmethod
    def get_label(node):
        return node.__class__.__name__


def compare_nodes(n1, n2):
    if type(n1) != type(n2):
        return False

    for (field1, value1), (field2, value2) in zip(ast.iter_fields(n1), ast.iter_fields(n2)):
        if field1 != field2:
            return False

        if isinstance(value1, list):
            if len(value1) != len(value2):
                return False
            for child1, child2 in zip(value1, value2):
                if not compare_nodes(child1, child2):
                    return False

        elif isinstance(value1, ast.AST):
            if not compare_nodes(value1, value2):
                return False

        else:
            if value1 != value2:
                return False

    return True

def expr_eq(node, vars):
    if node.__class__.__name__ == "BinOp":
        left = expr_eq(node.left, vars)
        right = expr_eq(node.right, vars)
        if left is not None and right is not None:
            if node.op.__class__.__name__ == "Add":
                return left + right
            elif node.op.__class__.__name__ == "Mult":
                return left * right
    elif node.__class__.__name__ == "Name":
        return vars.get(node.id, None)
    elif node.__class__.__name__ == "Constant":
        return ast.literal_eval(node)
    return None

def assign_eq(node, vars):
    if node.__class__.__name__ == "Assign":
        target = node.targets[0].id
        value = expr_eq(node.value, vars)
        if value is not None:
            vars[target] = value
            NodeVisitor.final_var = value

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
    n1 = ast.parse(open(fname1).read())
    n2 = ast.parse(open(fname2).read())
    if compare_nodes(n1, n2):
        print("The programs are identical")
    else:
        print("The programs are not identical")
    return -1

# Provide the solution to Exercise 3 by implementing the function below
def do_dst(fname1, fname2):
    n1 = ast.parse(open(fname1).read())
    n2 = ast.parse(open(fname2).read())
    dist = zss.simple_distance(n1, n2, NodeVisitor.get_children, NodeVisitor.get_label)
    v = NodeVisitor()
    v.visit(n1)
    n1_len = NodeVisitor.len
    NodeVisitor.len = 0
    v.visit(n2)
    n2_len = NodeVisitor.len
    normalized_dist = dist / (n1_len + n2_len)
    print(f"The normalized tree edit distance is {normalized_dist}")
    return -1

# Provide the solution to Exercise 4 by implementing the function below
def do_run(fname):
    node = ast.parse(open(fname).read())
    v = NodeVisitor()
    v.visit(node)
    print(f'The final value is {NodeVisitor.final_var}')
    return -1


if __name__ == "__main__":
    main()