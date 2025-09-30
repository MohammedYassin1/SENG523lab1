import sys
import ast

import re
from xmlrpc.client import boolean

class SecretAnalyzer(ast.NodeVisitor):

    varRegex = re.compile(r"(?i)(secret|password|key|token)")

    stringRegex = re.compile(r"^WOWSECRET_\d{2,5}_[A-Z]{4}$")

    @staticmethod
    def check_keyword(name):
        return bool(SecretAnalyzer.varRegex.search(name))
        
    @staticmethod
    def check_string(s):
        return bool(SecretAnalyzer.stringRegex.fullmatch(s))

    def visit_Assign(self, node):
        # print(f"Visiting Assign node at line {node.lineno}")
        for target in node.targets:
            if isinstance(target, ast.Name):
                if self.check_keyword(target.id):
                    #print(f"Found secret variable name: {target.id} at line {node.lineno}")
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        if self.check_string(node.value.value):
                            #print(f"Found secret string constant: {node.value.value} at line {node.lineno}")
                            print(f"Variable {target.id} assigned possible secret {node.value.value}")
        return self.generic_visit(node)

    def generic_visit(self, node):
        return super().generic_visit(node)
    
def tainted_equation(node):
    if isinstance(node, ast.Call):
        return node
            # for arg in node.args:
            #     if isinstance(arg, ast.Name) and arg.id in TaintAnalyzer.tainted_vars:
            #         print("fuck")
            #         return True
    if isinstance(node, ast.Name):
        return node
    if isinstance(node, ast.Constant):
        return node
    if isinstance(node, ast.BinOp):
        left = tainted_equation(node.left)
        right = tainted_equation(node.right)
        # print(f"Binary operation {ast.dump(node)}")
        # print(TaintAnalyzer.tainted_vars)
        # print(f"Left: {ast.dump(node.left)}, Right: {ast.dump(node.right)}")
        # print(f"Left: {ast.dump(left)}, Right: {ast.dump(right)}")

        if type(left) is bool:
            return left
        if type(right) is bool:
            return right

        if isinstance(left, ast.Call) or isinstance(right, ast.Call):
            if isinstance(left, ast.Call):
                for arg in left.args:
                    if isinstance(arg, ast.Name) and arg.id in TaintAnalyzer.tainted_vars:
                        return True
            if isinstance(right, ast.Call):
                for arg in right.args:
                    if isinstance(arg, ast.Name) and arg.id in TaintAnalyzer.tainted_vars:
                        return True
        left_tainted = isinstance(left, ast.Name) and left.id in TaintAnalyzer.tainted_vars
        right_tainted = isinstance(right, ast.Name) and right.id in TaintAnalyzer.tainted_vars
        # if isinstance(right, ast.BinOp):
        #     print("loc1")
        # if right.id in TaintAnalyzer.tainted_vars:
        #     print("loc2")
        # print(f"Left tainted: {left_tainted}, Right tainted: {right_tainted}")
        return left_tainted or right_tainted
    return False
    
class TaintAnalyzer(ast.NodeVisitor):

    sinks = {"os.system"}

    sources = {"input"}

    tainted_vars = set()

    def visit_Assign(self, node):
        # print(f"Visiting Assign node at line {node.lineno}")
        # print(ast.dump(node.value))
        # for target in node.targets:
            # print(f"Assignment to {ast.dump(target)}")
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id in self.sources:
                    for target in node.targets:
                        if isinstance(target, ast.Tuple):
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    self.tainted_vars.add(elt.id)
                                    # print(f"Variable {elt.id} is tainted from source {node.value.func.id}")
                        if isinstance(target, ast.Name):
                            self.tainted_vars.add(target.id)
                            # print(f"Variable {target.id} is tainted from source {node.value.func.id}")
                    # print(f"Found taint source {node.value.func.id}")
        if isinstance(node.value, ast.Name):
            if node.value.id in self.tainted_vars:
                for target in node.targets:
                    if isinstance(target, ast.Tuple):
                        for elt in target.elts:
                            if isinstance(elt, ast.Name):
                                self.tainted_vars.add(elt.id)
                                # print(f"Variable {elt.id} is tainted from variable {node.value.id}")
                    if isinstance(target, ast.Name):
                        self.tainted_vars.add(target.id)
                        # print(f"Variable {target.id} is tainted from variable {node.value.id}")
                # print(f"Assignment from variable {node.value.id}")
        if isinstance(node.value, ast.BinOp):
            if tainted_equation(node.value):
                # print("Taint")
                for target in node.targets:
                    if isinstance(target, ast.Tuple):
                        for elt in target.elts:
                            if isinstance(elt, ast.Name):
                                self.tainted_vars.add(elt.id)
                                # print(f"Variable {elt.id} is tainted from binary operation")
                    if isinstance(target, ast.Name):
                        self.tainted_vars.add(target.id)
                        # print(f"Variable {target.id} is tainted from binary operation")
            # else:
            #     print("No Taint")
            # print(f"Binary operation {tainted_equation(node.value)}")
            # left = node.value.left
            # right = node.value.right
            # left_tainted = isinstance(left, ast.Name) and left.id in self.tainted_vars
            # right_tainted = isinstance(right, ast.Name) and right.id in self.tainted_vars
            # if left_tainted or right_tainted:
            #     for target in node.targets:
            #         if isinstance(target, ast.Tuple):
            #             for elt in target.elts:
            #                 if isinstance(elt, ast.Name):
            #                     self.tainted_vars.add(elt.id)
            #                     # print(f"Variable {elt.id} is tainted from binary operation")
            #         if isinstance(target, ast.Name):
            #             self.tainted_vars.add(target.id)
                        # print(f"Variable {target.id} is tainted from binary operation")
                # print(f"Assignment from binary operation with tainted variable")
        
        if isinstance(node.value, ast.Call):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name):
                    if node.value.func.id == "sanitized":
                        return self.generic_visit(node)
                        #return
                        # self.tainted_vars.remove(node.value.args[0].id)


            for arg in node.value.args:
                if isinstance(arg, ast.Name) and arg.id in self.tainted_vars:
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.tainted_vars.add(target.id)
                            # print(f"Variable {target.id} is tainted from function argument {args.id}")
                    # print(f"Function argument {args.id} is tainted")
                    
            
        
        return self.generic_visit(node)
    
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                func_name = f"{node.value.func.value.id}.{node.value.func.attr}"
                if func_name in self.sinks:
                    for arg in node.value.args:
                        if isinstance(arg, ast.Name) and arg.id in self.tainted_vars:
                            # print(f"Tainted variable {arg.id} used in sink function {func_name} at line {node.lineno}")
                            # print(f"Sink function call: {ast.dump(node)}")
                            print("Unsafe data flow between source and sink detected")

    def generic_visit(self, node):
        # print(f"visiting {type(node).__name__}")
        return super().generic_visit(node)

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
    tree1 = ast.parse(open(fname).read())
    #print(ast.dump(tree1, indent=4))
    analyzer = SecretAnalyzer()
    analyzer.visit(tree1)
    # f = "WOWSECRET_124_ABSD"
    # if SecretAnalyzer.check_keyword(f):
    #     print("Matched!")
    # if SecretAnalyzer.check_string(f):
    #     print("Matched!")
    # print("SECRET not implemented")
    return -1

# Exercise 5
def do_taint(fname):
    tree1 = ast.parse(open(fname).read())
    # print(ast.dump(tree1, indent=4))
    analyzer = TaintAnalyzer()
    analyzer.visit(tree1)
    # print(f"Tainted variables: {TaintAnalyzer.tainted_vars}")
    # print("TAINT not implemented")
    return -1


if __name__ == "__main__":
    main()
