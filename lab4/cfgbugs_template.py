import ast
from typing import List, Set, Optional, Dict
import sys

# Global counter for BasicBlock IDs
_basic_block_counter = -1

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
    SOURCE = "source"
    SINK = "sink"
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
                return f"BB{_basic_block_counter}"
            else:
                return block.id

        block_lines.append(f"\tPredecessors: {', '.join(sorted(format_block_id(pred) for pred in self.predecessors))}")
        block_lines.append(f"\tSuccessors: {', '.join(sorted(format_block_id(succ) for succ in self.successors))}")

        return "\n".join(block_lines)
    
    def reaching_definitions_str(self):
        block_lines = [f"Basic Block {self.id}:"]
        
        # Format gen_set
        gen_items = ""
        if hasattr(self, 'gen_set') and self.gen_set:
            gen_list = [f"({var}, {block_id})" for var, block_id in sorted(self.gen_set, key=lambda x: (x[1], x[0]))]
            gen_items = f" {', '.join(gen_list)}"
        block_lines.append(f"\tgens:{gen_items}")
        
        # Format kill_set 
        kill_items = ""
        if hasattr(self, 'kill_set') and self.kill_set:
            kill_list = [f"({var}, {block_id})" for var, block_id in sorted(self.kill_set, key=lambda x: (x[1], x[0]))]
            kill_items = f" {', '.join(kill_list)}"
        block_lines.append(f"\tkills:{kill_items}")
        
        # Format in_set 
        in_items = ""
        if hasattr(self, 'in_rd') and self.in_rd:
            in_list = [f"({var}, {block_id})" for var, block_id in sorted(self.in_rd, key=lambda x: (x[1], x[0]))]
            in_items = f"{', '.join(in_list)}"
        block_lines.append(f"\tin: {in_items}")
        
        # Format out_set 
        out_items = ""
        if hasattr(self, 'out_rd') and self.out_rd:
            out_list = [f"({var}, {block_id})" for var, block_id in sorted(self.out_rd, key=lambda x: (x[1], x[0]))]
            out_items = f"{', '.join(out_list)}"
        block_lines.append(f"\tout: {out_items}")
        
        def format_block_id(block):
            if block.id == "Entry":
                return "BB0"
            elif block.id == "Exit":
                return f"BB{_basic_block_counter}"
            else:
                return block.id

        block_lines.append(f"\tPredecessors: {','.join(sorted([format_block_id(pred) for pred in self.predecessors]))}")
        block_lines.append(f"\tSuccessors: {', '.join(sorted([format_block_id(succ) for succ in self.successors]))}")

        return "\n".join(block_lines)

    def __str__(self):
        if self.id == "Entry":
            block_lines = [f"Basic Block BB0: {self.id}"]
        elif self.id == "Exit":
            block_lines = [f"Basic Block BB{_basic_block_counter}: {self.id}"] 
        else:
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
                return f"BB{_basic_block_counter}" 
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

    def add_block(self, block: BasicBlock):
        self.blocks.add(block)

    def add_edge(self, from_block: BasicBlock, to_block: BasicBlock):
        from_block.successors.add(to_block)
        to_block.predecessors.add(from_block)

    def cfg_print(self):
        def sort_key(block):
            if block.id == "Entry":
                return (0, 0)
            if block.id == "Exit":
                return (2, 0)
            
            try:
                bb_number = int(block.id[2:])
            except:
                bb_number = sys.maxsize
                
            return (1, bb_number)

        sorted_blocks = sorted(list(self.blocks), key=sort_key)
        for block in sorted_blocks:
            print(block)

    def cfg_printex2(self):
        print(f"Basic Block BB0: {self.entry.id}\n\tPredecessors:\n\tSuccessors: {', '.join(succ.id for succ in self.entry.successors)}")
        for block in sorted(self.blocks, key=lambda b: b.id):
            if block.id not in ("Entry", "Exit"):
                print(block.liveness_str())
        print(f"Basic Block BB{_basic_block_counter}: {self.exit.id}\n\tPredecessors: {', '.join(pred.id for pred in self.exit.predecessors)}\n\tSuccessors:")

    def cfg_printex3(self):
        print(f"Basic Block BB0: {self.entry.id}\n\tPredecessors:\n\tSuccessors: {', '.join(succ.id for succ in self.entry.successors)}")
        for block in sorted(self.blocks, key=lambda b: b.id):
            if block.id not in ("Entry", "Exit"):
                print(block.reaching_definitions_str())
        print(f"Basic Block BB{_basic_block_counter}: {self.exit.id}\n\tPredecessors: {', '.join(pred.id for pred in self.exit.predecessors)}\n\tSuccessors:")

class Builder(ast.NodeVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.current_block = cfg.entry

    def _get_exit_blocks(self, cfg: ControlFlowGraph):
        # Exit blocks are those without successors (i.e., tails)
        return [b for b in cfg.blocks if len(b.successors) == 0]
    
    def _any_block_has_statements(self, blocks):
        return any(len(b.statements) > 0 for b in blocks)
    
    

    def visit_Assign(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.ASSIGNMENT,
            def_set={node.targets[0].id},
            use_set=get_uses(node.value),
            ast_node=node
        ))

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            # use_set = set()
            # for arg in node.args:
            #     if isinstance(arg, ast.Name):
            #         use_set.add(arg.id)
            self.current_block.add_statement(Statement(
                stmt_type=StatementType.PRINT,
                def_set=set(),
                use_set=get_uses(node),
                ast_node=node
            ))
        
        elif isinstance(node.func, ast.Name) and node.func.id == "source":
            self.current_block.add_statement(Statement(
                stmt_type=StatementType.SOURCE,
                def_set=set(),
                use_set=set(),
                ast_node=node
            ))

        elif isinstance(node.func, ast.Name) and node.func.id == "sink":
            self.current_block.add_statement(Statement(
                stmt_type=StatementType.SINK,
                def_set=set(),
                use_set=get_uses(node),
                ast_node=node
            ))

    def visit_If(self, node):
        # Add IF condition into current block
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.IF,
            def_set=set(),
            use_set=get_uses(node.test),
            ast_node=node
        ))

        parent_block = self.current_block

        then_module = ast.Module(body=node.body, type_ignores=[])
        then_cfg = make_cfg(then_module)
        self.cfg.blocks.update(then_cfg.blocks)
        self.cfg.add_edge(parent_block, then_cfg.entry)
        then_exits = [b for b in then_cfg.blocks if len(b.successors) == 0]

        if node.orelse:
            else_module = ast.Module(body=node.orelse, type_ignores=[])
            else_cfg = make_cfg(else_module)
            self.cfg.blocks.update(else_cfg.blocks)
            self.cfg.add_edge(parent_block, else_cfg.entry)
            else_exits = [b for b in else_cfg.blocks if len(b.successors) == 0]
        else:
            else_exits = [parent_block]
        
        all_exits = then_exits + else_exits
        merge_block = None    

        for b in all_exits:
            if b is not parent_block and not b.statements:
                merge_block = b
                break

        if merge_block is None:
            merge_block = BasicBlock()
            self.cfg.add_block(merge_block)
            
            for b in all_exits:
                self.cfg.add_edge(b, merge_block)
        else:
            all_other_exits = [b for b in all_exits if b is not merge_block]
            
            for b in all_other_exits:
                self.cfg.add_edge(b, merge_block)

        self.current_block = merge_block

    def visit_While(self, node):
        parent_block = self.current_block

        cond_block = BasicBlock()
        self.cfg.add_block(cond_block)
        self.cfg.add_edge(parent_block, cond_block)

        cond_block.add_statement(Statement(
            stmt_type=StatementType.WHILE,
            def_set=set(),
            use_set=get_uses(node.test),
            ast_node=node
        ))

        body_module = ast.Module(body=node.body, type_ignores=[])
        body_cfg = make_cfg(body_module)
        self.cfg.blocks.update(body_cfg.blocks)
        self.cfg.add_edge(cond_block, body_cfg.entry)

        body_exits = [b for b in body_cfg.blocks if len(b.successors) == 0]
        for b in body_exits:
            self.cfg.add_edge(b, cond_block)

        if node.orelse:
            else_module = ast.Module(body=node.orelse, type_ignores=[])
            else_cfg = make_cfg(else_module)
            self.cfg.blocks.update(else_cfg.blocks)
            
            self.cfg.add_edge(cond_block, else_cfg.entry)
            else_exits = [b for b in else_cfg.blocks if len(b.successors) == 0]
            fallthrough_exits = else_exits
        else:
            fallthrough_exits = [cond_block]

        
        merge_block = None
        
        for b in fallthrough_exits:
            if b is not cond_block and not b.statements:
                merge_block = b
                break
        
        if merge_block is None:
            merge_block = BasicBlock()
            self.cfg.add_block(merge_block)

            for b in fallthrough_exits:
                self.cfg.add_edge(b, merge_block)
        else:
            all_other_exits = [b for b in fallthrough_exits if b is not merge_block]
            
            for b in all_other_exits:
                self.cfg.add_edge(b, merge_block)

        self.current_block = merge_block

class SingleStatementBuilder(ast.NodeVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.current_block = cfg.entry

    def visit_Assign(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.ASSIGNMENT,
            def_set={node.targets[0].id},
            use_set=get_uses(node.value),
            ast_node=node
        ))

        new_block = BasicBlock()
        self.cfg.add_edge(self.current_block, new_block)
        self.current_block = new_block
        self.cfg.add_block(self.current_block)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.current_block.add_statement(Statement(
                stmt_type=StatementType.PRINT,
                def_set=set(),
                use_set=get_uses(node),
                ast_node=node
            ))
        
        elif isinstance(node.func, ast.Name) and node.func.id == "source":
            self.current_block.add_statement(Statement(
                stmt_type=StatementType.SOURCE,
                def_set=set(),
                use_set=set(),
                ast_node=node
            ))

        elif isinstance(node.func, ast.Name) and node.func.id == "sink":
            self.current_block.add_statement(Statement(
                stmt_type=StatementType.SINK,
                def_set=set(),
                use_set=get_uses(node),
                ast_node=node
            ))

        new_block = BasicBlock()
        self.cfg.add_edge(self.current_block, new_block)
        self.current_block = new_block
        self.cfg.add_block(self.current_block)

    def visit_If(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.IF,
            def_set=set(),
            use_set=get_uses(node.test),
            ast_node=node
        ))

        new_block = BasicBlock()
        self.cfg.add_edge(self.current_block, new_block)
        self.current_block = new_block
        self.cfg.add_block(self.current_block)

    def visit_While(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.WHILE,
            def_set=set(),
            use_set=get_uses(node.test),
            ast_node=node
        ))

        new_block = BasicBlock()
        self.cfg.add_edge(self.current_block, new_block)
        self.current_block = new_block
        self.cfg.add_block(self.current_block)

def make_cfg(ast_node: ast.AST) -> ControlFlowGraph:
    """
    Constructs a Control Flow Graph (CFG) from the given AST node (tree or subtree).
    Returns a ControlFlowGraph instance representing the CFG.
    """
    cfg = ControlFlowGraph()
    # entry block
    cfg.entry = BasicBlock()
    cfg.add_block(cfg.entry)

    builder = Builder(cfg)
    builder.current_block = cfg.entry

    if hasattr(ast_node, "body") and isinstance(ast_node.body, list):
        stmts = ast_node.body
    else:
        stmts = []

    for stmt in stmts:
        builder.visit(stmt)

    # The CFG's "exit" is whatever builder.current_block ended up being.
    cfg.exit = builder.current_block
    return cfg

def make_cfg_manager(ast_node: ast.AST) -> ControlFlowGraph:
    """
    Constructs a Control Flow Graph (CFG) using a manager from the given AST node (tree or subtree).
    Returns a ControlFlowGraph instance representing the CFG.
    """
    entry = EntryBlock()
    
    cfg = make_cfg(ast_node)
    
    inner_exit_block = cfg.exit
    
    if not inner_exit_block.statements:
        final_exit = ExitBlock()
        
        for pred_block in list(inner_exit_block.predecessors):
            if inner_exit_block in pred_block.successors:
                pred_block.successors.remove(inner_exit_block)
            
            cfg.add_edge(pred_block, final_exit)
            
        if inner_exit_block in cfg.blocks:
            cfg.blocks.remove(inner_exit_block)
            
    else:
        final_exit = ExitBlock()
        
        cfg.add_edge(inner_exit_block, final_exit)

    cfg.add_block(entry)
    cfg.add_edge(entry, cfg.entry)
    cfg.entry = entry

    cfg.add_block(final_exit)
    cfg.exit = final_exit
    
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

def missing_return(cfg: ControlFlowGraph):
    for block in cfg.blocks:
        for stmt in block.statements:
            if stmt.stmt_type == StatementType.RETURN:
                block.remove_edge(cfg.exit)
    
    for block in cfg.blocks:
        block.in_set = set()
        block.out_set = set()
    
    changed = True
    while changed:
        changed = False
        for bb in cfg.blocks:
            old_in = bb.in_set.copy()
            old_out = bb.out_set.copy()

            # update in set
            new_in = set()
            for pred in bb.predecessors:
                new_in = new_in | pred.out_set
            bb.in_set = new_in

            # update out set
            bb.out_set = bb.in_set

            # check if changed
            if bb.in_rd != old_in or bb.out_rd != old_out:
                changed = True
    
    if cfg.exit.in_set:
        print("Missing return statement(s) detected.")

def taint_analysis(cfg: ControlFlowGraph):

    # remove entry and exit blocks
    # cfg.blocks.discard(cfg.entry)
    # cfg.blocks.discard(cfg.exit)

    # cfg.entry.successors.clear()
    # cfg.exit.predecessors.clear()

    for each_block in cfg.blocks:
        each_block.in_set = set()
        each_block.out_set = set()
    
    changed = True

    while changed:
        changed = False
        for bb in cfg.blocks:

            if bb.id == "Entry" or bb.id == "Exit":
                # changed = True
                continue

            old_in = bb.in_set.copy()
            old_out = bb.out_set.copy()

            # update in set
            new_in = set()
            for pred in bb.predecessors:
                new_in = new_in | pred.out_set
            bb.in_set = new_in

            # # update out set
            # bb.out_set = bb.in_set.copy()

            # for stmt in bb.statements:
            #     if stmt.stmt_type == StatementType.ASSIGNMENT:
            #         for var in stmt.def_set:
            #             if var in bb.out_set:
            #                 bb.out_set.remove(var)
            #     for var in stmt.use_set:
            #         bb.out_set.add(var)

            for stmt in bb.statements:
                if stmt.stmt_type == StatementType.SINK:
                    for var in stmt.use_set:
                        if var in bb.in_set:
                            print(f"Tainted data reached sink in block {bb.id} via variable '{var}'")
                elif stmt.stmt_type == StatementType.ASSIGNMENT:
                    for var in stmt.def_set:
                        if var in bb.in_set:
                            bb.out_set.add(var)
                        else:
                            if var in bb.out_set:
                                bb.out_set.remove(var)
                elif stmt.stmt_type == StatementType.SOURCE:
                    for var in stmt.def_set:
                        bb.out_set.add(var)

            # check if changed
            if bb.in_set != old_in or bb.out_set != old_out:
                changed = True
        print("Taint Analysis Results:")
        for block in sorted(cfg.blocks, key=lambda b: b.id):
            print(f"Basic Block {block.id}:")
            print(f"\tIn: {block.in_set}")
            print(f"\tOut: {block.out_set}")
        input("Press Enter to continue...")

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
    #print("RETURNS not implemented")
    tree = ast.parse(open(fname).read(), filename=fname)
    my_cfg = make_cfg(tree)

    missing_return(my_cfg)
    return -1

# Exercise 3
def do_taints(fname):
    # print("TAINTS not implemented")
    tree = ast.parse(open(fname).read(), filename=fname)
    my_cfg = make_cfg_manager(tree)
    my_cfg.cfg_print()

    # Perform taint analysis
    # taint_analysis(my_cfg)
    return -1


if __name__ == "__main__":
    main()
