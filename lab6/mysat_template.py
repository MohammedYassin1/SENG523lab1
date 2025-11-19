import sys
import ast
from graphviz import Digraph
import itertools

class LogicNode:
    def __init__(self, ntype, nsym):
        # Possible ntype values are AND, OR, NOT, IMPL
        self.ntype = ntype
        self.nsym = nsym
        self.op1 = None
        self.op2 = None

    def to_string(self, indent_level=0, node_str=None):
        if not node_str:
            node_str = ""
        node_str += (" " * indent_level)
        if self.ntype != "SYM":
            node_str += (f"{self.ntype} OPERATOR\n")
        else:
            node_str += (f"{self.nsym} SYMBOL\n")
        if self.op1:
            node_str = self.op1.to_string(indent_level+2, node_str)
        if self.op2:
            node_str = self.op2.to_string(indent_level+2, node_str)
        return node_str
    
class Builder(ast.NodeVisitor):
    def __init__(self):
        self.root = None

    def generic_visit(self, node):
        # print(f"Visiting node type: {type(node).__name__}")
        return super().generic_visit(node)
    
    def visit_Call(self, node):
        func_name = node.func.id
        # print(f"Visiting function call: {func_name}")
        if func_name == "AND":
            logic_node = LogicNode("AND", None)
        elif func_name == "OR":
            logic_node = LogicNode("OR", None)
        elif func_name == "NOT":
            logic_node = LogicNode("NOT", None)
        elif func_name == "IMPL":
            logic_node = LogicNode("IMPL", None)
        else:
            raise ValueError(f"Unknown function: {func_name}")
        
        if self.root is None:
            self.root = logic_node
        
        if len(node.args) >= 1:
            logic_node.op1 = self.visit(node.args[0])
        if len(node.args) == 2:
            logic_node.op2 = self.visit(node.args[1])

        # print(f"{logic_node.ntype}\n{logic_node.nsym}\n{logic_node.op1}\n{logic_node.op2}\n--------------------")
        
        # print(f"Constructed {logic_node.to_string()} node")
        # self.logic_tree.add_node(logic_node.ntype if logic_node.nsym is None else logic_node.nsym)
        return logic_node
    
    def visit_Name(self, node):
        # print(f"Visiting symbol: {node.id}")
        logic_node = LogicNode("SYM", node.id)
        # print(f"Constructed {logic_node.to_string()} node")
        return logic_node

def build_visualizer_tree(logic_node, visualizer):

    if logic_node is None:
        return None
    
    label = logic_node.ntype if logic_node.nsym is None else logic_node.nsym
    node_id = visualizer.add_node(label)
    
    if logic_node.op1:
        child_id1 = build_visualizer_tree(logic_node.op1, visualizer)
        visualizer.add_edge(node_id, child_id1)
    if logic_node.op2:
        child_id2 = build_visualizer_tree(logic_node.op2, visualizer)
        visualizer.add_edge(node_id, child_id2)
    
    return node_id

class TreeVisualizer:
    def __init__(self):
        self.node_counter = 0
        try:
            self.graph = Digraph('Tree')
        except ImportError:
            print("Error: graphviz module not found. Please install it with 'pip install graphviz'")
            sys.exit(1)
    
    def add_node(self, label=None):
        """Add a node to the graph and return its ID"""
        node_id = f"node{self.node_counter}"
        self.node_counter += 1
        
        if label is None:
            label = node_id
        
        self.graph.node(node_id, label)
        return node_id
    
    def add_edge(self, parent_id, child_id):
        """Add an edge between two nodes"""
        self.graph.edge(parent_id, child_id)
    
    def render(self, output_file):
        """Render the graph to a PNG file"""
        try:
            # Remove .png extension if present, graphviz will add it
            base_name = output_file.replace('.png', '')
            self.graph.render(base_name, format='png', cleanup=True)
            print(f"Tree rendered to {output_file}")
        except Exception as e:
            print(f"Error rendering graph: {e}")

def collect_vars(node, vars_set):
    if node is None:
        return
    if node.ntype == "SYM":
        vars_set.add(node.nsym)
    if node.op1:
        collect_vars(node.op1, vars_set)
    if node.op2:
        collect_vars(node.op2, vars_set)


def eval_node(node, assignment):
    if node is None:
        return False
    if node.ntype == "SYM":
        return bool(assignment.get(node.nsym, False))
    if node.ntype == "NOT":
        return not eval_node(node.op1, assignment)
    if node.ntype == "AND":
        return eval_node(node.op1, assignment) and eval_node(node.op2, assignment)
    if node.ntype == "OR":
        return eval_node(node.op1, assignment) or eval_node(node.op2, assignment)
    if node.ntype == "IMPL":
        a = eval_node(node.op1, assignment)
        b = eval_node(node.op2, assignment)
        return (not a) or b
    
def main():
    if len(sys.argv) != 3:
        print("Usage: python mysat.py <operation> <input_file>")
        sys.exit(1)
    elif sys.argv[1] == "parse":
        parse(sys.argv[2])
    elif sys.argv[1] == "visualize":
        visualize(sys.argv[2])
    elif sys.argv[1] == "evaluate":
        evaluate(sys.argv[2])
    elif sys.argv[1] == "solve":
        solve(sys.argv[2])
    else:
        print("Usage: python mysat.py <operation> <input_file>")
        sys.exit(1)

def parse(input_file):
    ast_tree = ast.parse(open(input_file).read())
    builder = Builder()
    builder.visit(ast_tree)
    # print(builder.root.to_string())
    return builder.root


def visualize(input_file):
    parse_tree = parse(input_file)
    # print(parse_tree.to_string())
    visualizer = TreeVisualizer()
    build_visualizer_tree(parse_tree, visualizer)
    visualizer.render(f"{input_file.replace('.py', '')}_output.png")
    return 0


def evaluate(input_file):
    return 0


def solve(input_file):
    root = parse(input_file)

    vars_set = set()
    collect_vars(root, vars_set)
    vars_list = sorted(vars_set)
    found = False
    for combo in itertools.product([True, False], repeat=len(vars_list)):
        assignment = dict(zip(vars_list, combo))

        if eval_node(root, assignment):
            pairs = [f"{v}: {assignment[v]}" for v in vars_list]
            print("SAT: " + ", ".join(pairs))
            found = True
            break

    if not found:
        print("UNSAT")
    return 0


if __name__ == "__main__":
    main()
