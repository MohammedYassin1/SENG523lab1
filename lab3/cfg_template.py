import ast
from typing import List, Set, Optional, Dict
import sys

# Global counter for BasicBlock IDs
_basic_block_counter = -2

def _next_basic_block_id():
    global _basic_block_counter
    _basic_block_counter += 1
    return f"BB{_basic_block_counter}"

class StatementType:
    ASSIGNMENT = "Assignment"
    IF = "If"
    WHILE = "While"
    PRINT = "Print"
    RETURN = "Return"
    OTHER = "Other"

class Statement:
    def __init__(self, stmt_type: str, def_set: Set[str], use_set: Set[str], ast_node: ast.AST):
        self.stmt_type: str = stmt_type
        self.def_set: Set[str] = def_set
        self.use_set: Set[str] = use_set
        self.ast_node: ast.AST = ast_node

class BasicBlock:
    def __init__(self):
        self.id: str = _next_basic_block_id()
        self.statements: List[Statement] = []
        self.def_set: Set[str] = set()
        self.use_set: Set[str] = set()
        self.predecessors: Set['BasicBlock'] = set()
        self.successors: Set['BasicBlock'] = set()

    def add_statement(self, stmt: Statement):
        self.statements.append(stmt)
        self.def_set.update(stmt.def_set)
        self.use_set.update(stmt.use_set)

    def __str__(self):
        # if self.id == "Entry":
        #     return ""
        #     return f"Basic Block BB0: {self.id}\n\tPredecessors:\n\tSuccessors: {', '.join(succ.id for succ in self.successors)}"
        # if self.id == "Exit":
        #     return ""
        #     return f"Basic Block {_next_basic_block_id()}: {self.id}"
        
        block_lines = [f"Basic Block {self.id}:"]
        block_lines.append(f"\tStatements:")
        for stmt in self.statements:
              def_items = f" {','.join(stmt.def_set)}" if stmt.def_set else ""
              use_items = f" {','.join(stmt.use_set)}" if stmt.use_set else ""
              block_lines.append(f"\t\t{stmt.stmt_type}: defs:{def_items}; uses:{use_items}")
        def format_block_id(block):
            if block.id == "Entry":
                return "BB0"
            elif block.id == "Exit":
                return f"BB{_basic_block_counter+1}"
            else:
                return block.id

        block_lines.append(f"\tPredecessors: {', '.join(format_block_id(pred) for pred in self.predecessors)}")
        block_lines.append(f"\tSuccessors: {', '.join(format_block_id(succ) for succ in self.successors)}")

        return "\n".join(block_lines)

class EntryBlock(BasicBlock):
    def __init__(self):
        super().__init__()
        self.id = "Entry"

class ExitBlock(BasicBlock):
    def __init__(self):
        super().__init__()
        self.id = "Exit"

class ControlFlowGraph:
    def __init__(self):
        self.blocks: Set[BasicBlock] = set()
        self.entry: EntryBlock = EntryBlock()
        self.exit: ExitBlock = ExitBlock()
        self.blocks.add(self.entry)
        self.blocks.add(self.exit)

    def add_block(self, block: BasicBlock):
        self.blocks.add(block)

    def add_edge(self, from_block: BasicBlock, to_block: BasicBlock):
        from_block.successors.add(to_block)
        to_block.predecessors.add(from_block)

    def cfg_print(self):
        print(f"Basic Block BB0: {self.entry.id}\n\tPredecessors:\n\tSuccessors: {', '.join(succ.id for succ in self.entry.successors)}")
        for block in sorted(self.blocks, key=lambda b: b.id):
            if block.id not in ("Entry", "Exit"):
                print(block)
        print(f"Basic Block {_next_basic_block_id()}: {self.exit.id}\n\tPredecessors: {', '.join(pred.id for pred in self.exit.predecessors)}\n\tSuccessors:")

class Builder(ast.NodeVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.current_block: Optional[BasicBlock] = cfg.entry

    # def __str__(self):
    #     return f"Builder(current_block={self.current_block})"

    # def visit_Module(self, node):
    #     for stmt in node.body:
    #         self.current_block = self.visit(stmt)

    #     if (self.current_block and self.cfg.exit not in self.current_block.successors):
    #         self.cfg.add_edge(self.current_block, self.cfg.exit)

    def visit_Assign(self, node):
        # print(f"Visiting Assign: {ast.dump(node)}")
        if self.current_block == self.cfg.entry:
            print("Creating first basic block")
            self.current_block = BasicBlock()
            self.cfg.add_block(self.current_block)
            self.cfg.add_edge(self.cfg.entry, self.current_block)

        # check if constant assignment
        # FIX: append to def and use sets
        if isinstance(node.value, ast.Constant):
            def_set = {node.targets[0].id}
            use_set = set()
        elif isinstance(node.value, ast.BinOp):
            def_set = {node.targets[0].id}
            use_set = set()
            if isinstance(node.value.left, ast.Name):
                use_set.add(node.value.left.id)
            if isinstance(node.value.right, ast.Name):
                use_set.add(node.value.right.id)
        
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.ASSIGNMENT,
            def_set=def_set,
            use_set=use_set,
            ast_node=node
        ))
        # return super().visit_Assign(node)
        return self.current_block

    def visit_Call(self, node):
        if self.current_block == self.cfg.entry:
            print("Creating first basic block")
            self.current_block = BasicBlock()
            self.cfg.add_block(self.current_block)
            self.cfg.add_edge(self.cfg.entry, self.current_block)

        # FIX: append to def and use sets
        # def_set = set()
        # use_set = set()
        # for arg in node.args:
        #     if isinstance(arg, ast.Name):
        #         use_set.add(arg.id)

        if isinstance(node.func, ast.Name) and node.func.id == "print":
            def_set = set()
            use_set = set(get_uses(node))
        
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.PRINT,
            def_set=def_set,
            use_set=use_set,
            ast_node=node
        ))
        # return super().visit_Call(node)
        return self.current_block

    def visit_While(self, node):
        old_block = self.current_block
        self.current_block = BasicBlock()
        self.cfg.add_block(self.current_block)
        self.cfg.add_edge(old_block, self.current_block)

        # check if variable used in while condition
        # use_set = set()
        # if isinstance(node.test, ast.Compare):
        #     if isinstance(node.test.left, ast.Name):
        #         use_set.add(node.test.left.id)
        #     for comparator in node.test.comparators:
        #         if isinstance(comparator, ast.Name):
        #             use_set.add(comparator.id)
        use_set = set(get_uses(node.test))

        self.current_block.add_statement(Statement(
            stmt_type=StatementType.WHILE,
            def_set=set(),
            use_set=use_set,
            ast_node=node
        ))

        while_block = self.current_block

        #then_block = BasicBlock()
        self.current_block = BasicBlock()
        self.cfg.add_edge(while_block, self.current_block)
        self.cfg.add_edge(self.current_block, while_block)  # back edge to while
        self.cfg.add_block(self.current_block)

        for stmt in node.body:
            self.current_block = self.visit(stmt)

        
        if node.orelse:
            for stmt in node.orelse:
                self.visit(stmt)

        self.current_block = BasicBlock()
        self.cfg.add_edge(while_block, self.current_block)
        self.cfg.add_block(self.current_block)

        

    def visit_If(self, node):
        old_block = self.current_block
        self.current_block = BasicBlock()
        self.cfg.add_block(self.current_block)
        self.cfg.add_edge(old_block, self.current_block)

        # check if variable used in if condition
        use_set = set(get_uses(node.test))

        self.current_block.add_statement(Statement(
            stmt_type=StatementType.IF,
            def_set=set(),
            use_set=use_set,
            ast_node=node
        ))

        if_block = self.current_block

        then_block = BasicBlock()

        self.current_block = then_block
        self.cfg.add_edge(if_block, self.current_block)
        self.cfg.add_block(self.current_block)

        for stmt in node.body:
            self.current_block = self.visit(stmt)
        then_exit = self.current_block

        if node.orelse:
            else_block = BasicBlock()
            self.current_block = else_block
            self.cfg.add_edge(if_block, self.current_block)
            self.cfg.add_block(self.current_block)

            for stmt in node.orelse:
                self.visit(stmt)

        self.current_block = BasicBlock()
        self.cfg.add_block(self.current_block)
        self.cfg.add_edge(then_exit, self.current_block)
        if node.orelse:
            self.cfg.add_edge(else_block, self.current_block)
        else:
            self.cfg.add_edge(if_block, self.current_block)

        return self.current_block


    def visit_Return(self, node):
        if self.current_block == self.cfg.entry:
            self.current_block = BasicBlock()
            self.cfg.add_block(self.current_block)
            self.cfg.add_edge(self.cfg.entry, self.current_block)

        def_set = set()
        use_set = set(get_uses(node))

        self.current_block.add_statement(Statement(
            stmt_type=StatementType.RETURN,
            def_set=def_set,
            use_set=use_set,
            ast_node=node
        ))

        self.cfg.add_edge(self.current_block, self.cfg.exit)
        # self.current_block = BasicBlock()
        # self.cfg.add_block(self.current_block)


    def generic_visit(self, node):
        return super().generic_visit(node)
    
def get_uses(node):
    """
    Recursively collect all variable names used in an AST expression.
    Works for nested BinOp, UnaryOp, Compare, BoolOp, etc.
    """
    if node is None:
        return []

    uses = set()

    # Case 1: Variable name
    if isinstance(node, ast.Name):
        uses.add(node.id)

    # Case 2: Binary operator (e.g., a + b)
    elif isinstance(node, ast.BinOp):
        uses.update(get_uses(node.left))
        uses.update(get_uses(node.right))

    # Case 3: Unary operator (e.g., -x)
    elif isinstance(node, ast.UnaryOp):
        uses.update(get_uses(node.operand))

    # Case 4: Comparison (e.g., x > 0 or a < b < c)
    elif isinstance(node, ast.Compare):
        uses.update(get_uses(node.left))
        for comp in node.comparators:
            uses.update(get_uses(comp))

    # Case 5: Boolean operations (e.g., a and b)
    elif isinstance(node, ast.BoolOp):
        for value in node.values:
            uses.update(get_uses(value))

    # Case 6: Function call (e.g., print(x))
    elif isinstance(node, ast.Call):
        # uses.update(get_uses(node.func))
        for arg in node.args:
            uses.update(get_uses(arg))

    # Case 7: Attribute (e.g., obj.attr) – usually the base is a variable
    elif isinstance(node, ast.Attribute):
        uses.update(get_uses(node.value))

    # Case 8: Subscript (e.g., arr[i])
    elif isinstance(node, ast.Subscript):
        uses.update(get_uses(node.value))
        uses.update(get_uses(node.slice))

    # Case 9: Constant or literal (ignore)
    elif isinstance(node, (ast.Constant)):
        pass

    # Case 10: Tuple, List, Set, Dict
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        for elt in node.elts:
            uses.update(get_uses(elt))
    elif isinstance(node, ast.Dict):
        for key, value in zip(node.keys, node.values):
            uses.update(get_uses(key))
            uses.update(get_uses(value))

    return list(uses)
    


def make_cfg(ast_node: ast.AST) -> ControlFlowGraph:
    """
    Constructs a Control Flow Graph (CFG) from the given AST node (tree or subtree).
    Returns a ControlFlowGraph instance representing the CFG.
    """
    cfg = ControlFlowGraph()
    # TODO: Traverse the AST and build basic blocks and edges.
    # This is a template; actual implementation should analyze the AST,
    # create Statement objects, group them into BasicBlocks, and connect blocks.
    visitor = Builder(cfg)
    visitor.visit(ast_node)

    if (
    visitor.current_block
    and visitor.current_block is not cfg.exit
    and cfg.exit not in visitor.current_block.successors
    ):
        cfg.add_edge(visitor.current_block, cfg.exit)

    return cfg


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "CFG":
        return do_CFG(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "liveness":
        return do_liveness(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "reaching":
        return do_reaching(sys.argv[2])
    else:
        print("Usage: python cfg.py <cmd> <file>")
        return -1
    
# Exercise 1
def do_CFG(fname):
    tree = ast.parse(open(fname).read(), filename=fname)
    # print(ast.dump(tree, indent=4))
    my_cfg = make_cfg(tree)
    my_cfg.cfg_print()
    # print("CFG not implemented")
    return -1

# Exercise 2
def do_liveness(fname):
    print("LIVENESS not implemented")
    return -1

# Exercise 3
def do_reaching(fname):
    print("REACHING not implemented")
    return -1


if __name__ == "__main__":
    main()
