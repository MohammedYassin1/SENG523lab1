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

        block_lines.append(f"\tPredecessors: {', '.join(sorted(format_block_id(pred) for pred in self.predecessors))}")
        block_lines.append(f"\tSuccessors: {', '.join(sorted(format_block_id(succ) for succ in self.successors))}")

        return "\n".join(block_lines)
    
    def liveness_str(self):
        # if self.id == "Entry":
        #     return ""
        #     return f"Basic Block BB0: {self.id}\n\tPredecessors:\n\tSuccessors: {', '.join(succ.id for succ in self.successors)}"
        # if self.id == "Exit":
        #     return ""
        #     return f"Basic Block {_next_basic_block_id()}: {self.id}"
        
        block_lines = [f"Basic Block {self.id}:"]
        #block_lines.append(f"\tStatements:")
        #for stmt in self.statements:
        def_items = f" {','.join(sorted(self.def_set))}" if self.def_set else ""
        use_items = f" {','.join(sorted(self.use_set))}" if self.use_set else ""
        block_lines.append(f"\tdefs:{def_items}")
        block_lines.append(f"\tuses:{use_items}")
        in_items = f"{','.join(sorted(self.in_set))}" if hasattr(self, 'in_set') and self.in_set else ""
        out_items = f"{','.join(sorted(self.out_set))}" if hasattr(self, 'out_set') and self.out_set else ""
        block_lines.append(f"\tin: {in_items}")
        block_lines.append(f"\tout: {out_items}")
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
    
    def reaching_definitions_str(self):
        block_lines = [f"Basic Block {self.id}:"]
        
        # Format gen_set (tuples of (variable, block_id))
        gen_items = ""
        if hasattr(self, 'gen_set') and self.gen_set:
            gen_list = [f"({var}, {block_id})" for var, block_id in sorted(self.gen_set, key=lambda x: (x[1], x[0]))]
            gen_items = f" {', '.join(gen_list)}"
        block_lines.append(f"\tgens:{gen_items}")
        
        # Format kill_set (tuples of (variable, block_id))
        kill_items = ""
        if hasattr(self, 'kill_set') and self.kill_set:
            kill_list = [f"({var}, {block_id})" for var, block_id in sorted(self.kill_set, key=lambda x: (x[1], x[0]))]
            kill_items = f" {', '.join(kill_list)}"
        block_lines.append(f"\tkills:{kill_items}")
        
        # Format in_set (tuples of (variable, block_id))
        in_items = ""
        if hasattr(self, 'in_rd') and self.in_rd:
            in_list = [f"({var}, {block_id})" for var, block_id in sorted(self.in_rd, key=lambda x: (x[1], x[0]))]
            in_items = f"{', '.join(in_list)}"
        block_lines.append(f"\tin: {in_items}")
        
        # Format out_set (tuples of (variable, block_id))
        out_items = ""
        if hasattr(self, 'out_rd') and self.out_rd:
            out_list = [f"({var}, {block_id})" for var, block_id in sorted(self.out_rd, key=lambda x: (x[1], x[0]))]
            out_items = f"{', '.join(out_list)}"
        block_lines.append(f"\tout: {out_items}")
        
        def format_block_id(block):
            if block.id == "Entry":
                return "BB0"
            elif block.id == "Exit":
                return f"BB{_basic_block_counter+1}"
            else:
                return block.id

        block_lines.append(f"\tPredecessors: {','.join(sorted([format_block_id(pred) for pred in self.predecessors]))}")
        block_lines.append(f"\tSuccessors: {', '.join(sorted([format_block_id(succ) for succ in self.successors]))}")

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

    def cfg_printex2(self):
        print(f"Basic Block BB0: {self.entry.id}\n\tPredecessors:\n\tSuccessors: {', '.join(succ.id for succ in self.entry.successors)}")
        for block in sorted(self.blocks, key=lambda b: b.id):
            if block.id not in ("Entry", "Exit"):
                print(block.liveness_str())
        print(f"Basic Block {_next_basic_block_id()}: {self.exit.id}\n\tPredecessors: {', '.join(pred.id for pred in self.exit.predecessors)}\n\tSuccessors:")

    def cfg_printex3(self):
        print(f"Basic Block BB0: {self.entry.id}\n\tPredecessors:\n\tSuccessors: {', '.join(succ.id for succ in self.entry.successors)}")
        for block in sorted(self.blocks, key=lambda b: b.id):
            if block.id not in ("Entry", "Exit"):
                print(block.reaching_definitions_str())
        print(f"Basic Block {_next_basic_block_id()}: {self.exit.id}\n\tPredecessors: {', '.join(pred.id for pred in self.exit.predecessors)}\n\tSuccessors:")

class Builder(ast.NodeVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.current_block: Optional[BasicBlock] = cfg.entry
        self.defer_join: bool = False  # for if-statements without else


    def visit_Assign(self, node):
        # print(f"Visiting Assign: {ast.dump(node)}")
        if self.current_block == self.cfg.entry:
            # print("Creating first basic block")
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
            # print("Creating first basic block")
            self.current_block = BasicBlock()
            self.cfg.add_block(self.current_block)
            self.cfg.add_edge(self.cfg.entry, self.current_block)

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
        cond_block = BasicBlock()
        self.cfg.add_block(cond_block)
        self.cfg.add_edge(old_block, cond_block)

        use_set = set(get_uses(node.test))
        cond_block.add_statement(Statement(
            stmt_type=StatementType.WHILE,
            def_set=set(),
            use_set=use_set,
            ast_node=node
        ))

        body_block = BasicBlock()
        self.cfg.add_block(body_block)
        self.cfg.add_edge(cond_block, body_block)

        # Enter loop body
        prev_inside_loop = getattr(self, "inside_loop", False)
        self.inside_loop = True

        self.current_block = body_block
        for stmt in node.body:
            self.current_block = self.visit(stmt)

        self.cfg.add_edge(self.current_block, cond_block)

        self.inside_loop = prev_inside_loop

        if node.orelse:
            else_block = BasicBlock()
            self.cfg.add_block(else_block)
            self.cfg.add_edge(cond_block, else_block)
            self.current_block = else_block
            for stmt in node.orelse:
                self.current_block = self.visit(stmt)
            exit_block = self.current_block
        else:
            exit_block = cond_block


        join_block = BasicBlock()
        self.cfg.add_block(join_block)
        self.cfg.add_edge(cond_block, join_block)
        if node.orelse:
            self.cfg.add_edge(exit_block, join_block)

        self.current_block = join_block
        return self.current_block

    
    def visit_If(self, node):
        if self.current_block == self.cfg.entry:
            self.current_block = BasicBlock()
            self.cfg.add_block(self.current_block)
            self.cfg.add_edge(self.cfg.entry, self.current_block)

        use_set = set(get_uses(node.test))
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.IF,
            def_set=set(),
            use_set=use_set,
            ast_node=node
        ))

        if_block = self.current_block

        then_block = BasicBlock()
        self.cfg.add_block(then_block)
        self.cfg.add_edge(if_block, then_block)

        prev_inside_loop = getattr(self, "inside_loop", False)

        self.current_block = then_block
        for stmt in node.body:
            self.current_block = self.visit(stmt)
        then_exit = self.current_block

        if node.orelse:
            else_block = BasicBlock()
            self.cfg.add_block(else_block)
            self.cfg.add_edge(if_block, else_block)
            self.current_block = else_block
            for stmt in node.orelse:
                self.current_block = self.visit(stmt)
            else_exit = self.current_block
        else:
            else_exit = None

        if prev_inside_loop:
            if else_exit:
                self.cfg.add_edge(else_exit, then_exit)
            self.current_block = then_exit
            return self.current_block

        join_block = BasicBlock()
        self.cfg.add_block(join_block)
        self.cfg.add_edge(then_exit, join_block)
        if else_exit:
            self.cfg.add_edge(else_exit, join_block)
        else:
            self.cfg.add_edge(if_block, join_block)

        self.current_block = join_block
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
    if node is None:
        return []

    uses = set()

    if isinstance(node, ast.Name):
        uses.add(node.id)

    elif isinstance(node, ast.BinOp):
        uses.update(get_uses(node.left))
        uses.update(get_uses(node.right))

    elif isinstance(node, ast.UnaryOp):
        uses.update(get_uses(node.operand))

    elif isinstance(node, ast.Compare):
        uses.update(get_uses(node.left))
        for comp in node.comparators:
            uses.update(get_uses(comp))

    elif isinstance(node, ast.BoolOp):
        for value in node.values:
            uses.update(get_uses(value))

    elif isinstance(node, ast.Call):
        # uses.update(get_uses(node.func))
        for arg in node.args:
            uses.update(get_uses(arg))

    elif isinstance(node, ast.Attribute):
        uses.update(get_uses(node.value))

    elif isinstance(node, ast.Subscript):
        uses.update(get_uses(node.value))
        uses.update(get_uses(node.slice))

    elif isinstance(node, (ast.Constant)):
        pass

    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        for elt in node.elts:
            uses.update(get_uses(elt))
    elif isinstance(node, ast.Dict):
        for key, value in zip(node.keys, node.values):
            uses.update(get_uses(key))
            uses.update(get_uses(value))

    if isinstance(node, ast.Return):
        uses.update(get_uses(node.value))

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

def make_queue(cfg: ControlFlowGraph):
    #create in and out set for each bb
    for bb in cfg.blocks:
        bb.in_set = set()
        bb.out_set = set()

    #create a queue to add all bbs to
    bb_queue = []
    bb_queue.append(cfg.entry)

    for bb in cfg.blocks:
        bb_queue.append(bb)

    bb_queue.append(cfg.exit)

    ##update in and out sets
    while bb_queue:
        #Pull a node from the head of the queue
        bb = bb_queue.pop(0)

        old_in = bb.in_set.copy()
        old_out = bb.out_set.copy()

        #update in and out sets

        if bb.successors:
            new_out = set()
            for successor in bb.successors:
                new_out = new_out | successor.in_set
            bb.out_set= new_out

        bb.in_set = bb.use_set | (bb.out_set - bb.def_set)

        if bb.in_set != old_in:
            for predecessor in bb.predecessors:
                if predecessor not in bb_queue:
                    bb_queue.append(predecessor)
                    
def reaching_definition(cfg: ControlFlowGraph):
    #create in and out set for each bb
    for bb in cfg.blocks:
        #initialize in, out, gen, kill sets
        bb.in_rd = set()
        bb.out_rd = set()
        bb.gen_set = set()
        bb.kill_set = set()
        temp = set()

    # compute gen and kill sets
        for stmt in bb.statements:
            for var in stmt.def_set:
                bb.gen_set.add((var, bb.id))
                temp.add(var)
        
        for other_bb in cfg.blocks:
            if other_bb is not bb:
                for stmt in other_bb.statements:
                    for var in stmt.def_set:
                        if var in temp:
                            bb.kill_set.add((var, other_bb.id))

    # iterative computation of in and out sets
    changed = True
    while changed:
        changed = False
        for bb in cfg.blocks:
            old_in = bb.in_rd.copy()
            old_out = bb.out_rd.copy()

            # update in set
            new_in = set()
            for pred in bb.predecessors:
                new_in = new_in | pred.out_rd
            bb.in_rd = new_in

            # update out set
            bb.out_rd = bb.gen_set | (bb.in_rd - bb.kill_set)

            # check if changed
            if bb.in_rd != old_in or bb.out_rd != old_out:
                changed = True

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
    tree = ast.parse(open(fname).read(), filename=fname)
    my_cfg = make_cfg(tree)
    make_queue(my_cfg)
    my_cfg.cfg_printex2()
    #print("LIVENESS not implemented")
    return -1

# Exercise 3
def do_reaching(fname):
    tree = ast.parse(open(fname).read(), filename=fname)
    my_cfg = make_cfg(tree)
    reaching_definition(my_cfg)
    my_cfg.cfg_printex3()
    #print("REACHING not implemented")
    return -1


if __name__ == "__main__":
    main()
