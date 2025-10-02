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


def make_cfg(ast_node: ast.AST) -> ControlFlowGraph:
    """
    Constructs a Control Flow Graph (CFG) from the given AST node (tree or subtree).
    Returns a ControlFlowGraph instance representing the CFG.
    """
    cfg = ControlFlowGraph()
    # TODO: Traverse the AST and build basic blocks and edges.
    # This is a template; actual implementation should analyze the AST,
    # create Statement objects, group them into BasicBlocks, and connect blocks.
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
    print("CFG not implemented")
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
