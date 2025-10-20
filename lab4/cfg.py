import ast
from typing import List, Set, Optional, Dict
import sys

# Global counter for BasicBlock IDs
_basic_block_counter = 0

def _next_basic_block_id():
    global _basic_block_counter
    _basic_block_counter += 1
    return f"BB{_basic_block_counter}"

class StatementType:
    ASSIGNMENT = "assignment"
    IF = "if"
    WHILE = "while"
    PRINT = "print"
    RETURN = "return"
    OTHER = "other"

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

        block_lines.append(f"\tPredecessors: {', '.join(sorted(format_block_id(pred) for pred in self.predecessors))}")
        block_lines.append(f"\tSuccessors: {', '.join(sorted(format_block_id(succ) for succ in self.successors))}")

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
        self.entry: EntryBlock = None
        self.exit: ExitBlock = None
        # self.blocks.add(self.entry)
        # self.blocks.add(self.exit)

    def add_block(self, block: BasicBlock):
        self.blocks.add(block)

    def add_edge(self, from_block: BasicBlock, to_block: BasicBlock):
        from_block.successors.add(to_block)
        to_block.predecessors.add(from_block)

    def cfg_print(self):
        for block in sorted(self.blocks, key=lambda b: b.id):
            print(block)

class Builder(ast.NodeVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.current_block = cfg.entry # BasicBlock()
        #self.cfg.add_block(self.current_block)

    # def generic_visit(self, node):
    #     return super().generic_visit(node)

    def visit_Assign(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.ASSIGNMENT,
            def_set={node.targets[0].id},
            use_set={node.value.id} if isinstance(node.value, ast.Name) else set(),
            ast_node=node
        ))

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            use_set = set()
            for arg in node.args:
                if isinstance(arg, ast.Name):
                    use_set.add(arg.id)
            self.current_block.add_statement(Statement(
                stmt_type=StatementType.PRINT,
                def_set=set(),
                use_set=use_set,
                ast_node=node
            ))

    def visit_If(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.IF,
            def_set=set(),
            use_set={node.test.id} if isinstance(node.test, ast.Name) else set(),
            ast_node=node
        ))
        # generate CFG for the body
        inner_cfg = make_cfg(node)

        # Integrate inner CFG into current CFG
        self.cfg.blocks.update(inner_cfg.blocks)

        # Connect current block to inner CFG entry
        self.cfg.add_edge(self.current_block, inner_cfg.entry)

        # After processing the if body, create a new block for subsequent statements
        old_block = self.current_block
        self.current_block = BasicBlock()
        self.cfg.add_block(self.current_block)

        # Connect all exit blocks of inner CFG to the new current block
        # for block in inner_cfg.blocks:
        #     if not block.successors:  # If it's an exit block
        #         self.cfg.add_edge(block, self.current_block)

        # self.cfg.add_edge(old_block, self.current_block)
        # self.cfg.add_edge(inner_cfg.entry, self.current_block)

    def visit_While(self, node):

        old_block = self.current_block
        self.current_block = BasicBlock()
        self.cfg.add_block(self.current_block)

        self.cfg.add_edge(old_block, self.current_block)

        self.current_block.add_statement(Statement(
            stmt_type=StatementType.WHILE,
            def_set=set(),
            use_set={node.test.id} if isinstance(node.test, ast.Name) else set(),
            ast_node=node
        ))
        # generate CFG for the body
        inner_cfg = make_cfg(node)

        # Integrate inner CFG into current CFG
        self.cfg.blocks.update(inner_cfg.blocks)

        # Connect current block to inner CFG entry
        self.cfg.add_edge(self.current_block, inner_cfg.entry)

        # After processing the while body, create a new block for subsequent statements
        old_block = self.current_block
        self.current_block = BasicBlock()
        self.cfg.add_block(self.current_block)

        # Connect all exit blocks of inner CFG to the new current block
        # for block in inner_cfg.blocks:
        #     if not block.successors:  # If it's an exit block
        #         self.cfg.add_edge(block, self.current_block)

        # self.cfg.add_edge(old_block, self.current_block)
        # self.cfg.add_edge(inner_cfg.entry, self.current_block)


def make_cfg(ast_node: ast.AST) -> ControlFlowGraph:
    """
    Constructs a Control Flow Graph (CFG) from the given AST node (tree or subtree).
    Returns a ControlFlowGraph instance representing the CFG.
    """
    cfg = ControlFlowGraph()
    cfg.entry = BasicBlock()
    cfg.add_block(cfg.entry)
    # cfg.exit = BasicBlock()
    # cfg.add_block(BasicBlock())
    builder = Builder(cfg)
    # builder.visit(ast_node)
    for stmt in ast_node.body:
        builder.visit(stmt)
    return cfg

def make_cfg_manager(ast_node: ast.AST) -> ControlFlowGraph:
    """
    Constructs a Control Flow Graph (CFG) using a manager from the given AST node (tree or subtree).
    Returns a ControlFlowGraph instance representing the CFG.
    """
    cfg = ControlFlowGraph()
    builder = Builder(cfg)
    builder.visit(ast_node)
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
    print(ast.dump(tree, indent=4))
    cfg = make_cfg(tree)
    cfg.cfg_print()
    return 0

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
