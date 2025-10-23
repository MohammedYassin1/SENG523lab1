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
        # Update use_set with uses that occur before any local definition
        for u in stmt.use_set:
            if u not in self.def_set:
                self.use_set.add(u)
        # Now update def_set with this statement's definitions
        self.def_set.update(stmt.def_set)

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
    
    def visit_AugAssign(self, node):
        # Handle augmented assignments like x -= 1
        target = None
        if isinstance(node.target, ast.Name):
            target = node.target.id
        uses = set()
        # augmented assign reads the target and the value
        if target:
            uses.add(target)
        uses.update(get_uses(node.value))
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.ASSIGNMENT,
            def_set={target} if target else set(),
            use_set=uses,
            ast_node=node
        ))

    def visit_Assign(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.ASSIGNMENT,
            def_set={node.targets[0].id},
            use_set=get_uses(node.value),
            ast_node=node
        ))

    def visit_Return(self, node):
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.RETURN,
            def_set=set(),
            use_set=set(get_uses(node)),
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
        # Record the if condition in the current block
        self.current_block.add_statement(Statement(
            stmt_type=StatementType.IF,
            def_set=set(),
            use_set=set(get_uses(node.test)),
            ast_node=node
        ))

        # Save reference to the block containing the IF statement
        if_block = self.current_block

        # --- THEN branch ---
        then_block = BasicBlock()
        self.cfg.add_block(then_block)
        # link current -> then_block
        if_block.successors.add(then_block)
        then_block.predecessors.add(if_block)

        # If the first statement of the then-branch is a While, set
        # current to then_block so visit_While can reuse it as the cond block.
        if node.body and isinstance(node.body[0], ast.While):
            self.current_block = then_block
            # visit each stmt in the then body; visit_While will handle blocks correctly
            for stmt in node.body:
                self.visit(stmt)
        else:
            # Otherwise visit the then branch normally starting from then_block
            self.current_block = then_block
            for stmt in node.body:
                self.visit(stmt)

        # Save end of then branch to link to next
        then_end_block = self.current_block

        # --- ELSE branch ---
        if node.orelse:
            else_block = BasicBlock()
            self.cfg.add_block(else_block)
            # connect from the IF's original block to else_block
            if_block.successors.add(else_block)
            else_block.predecessors.add(if_block)

            # visit else branch starting from else_block
            self.current_block = else_block
            for stmt in node.orelse:
                self.visit(stmt)
            else_end_block = self.current_block
        else:
            else_end_block = None

        # --- Create a join/continuation block ---
        join_block = BasicBlock()
        self.cfg.add_block(join_block)

        # link then_end -> join
        if not (then_end_block.statements and then_end_block.statements[-1].stmt_type == StatementType.RETURN):
            then_end_block.successors.add(join_block)
            join_block.predecessors.add(then_end_block)

        # link else_end -> join (if present)
        if else_end_block:
            if not (else_end_block.statements and else_end_block.statements[-1].stmt_type == StatementType.RETURN):
                else_end_block.successors.add(join_block)
                join_block.predecessors.add(else_end_block)
        else:
            if not (if_block.statements and if_block.statements[-1].stmt_type == StatementType.RETURN):
                if_block.successors.add(join_block)
                join_block.predecessors.add(if_block)

        # continue from the join
        self.current_block = join_block


    def visit_While(self, node):
        """
        Create a canonical loop header block for the while condition.
        If the current block is an empty connector (newly-created then-block),
        reuse it as the condition block. Otherwise allocate a fresh condition block.
        """

        cur = self.current_block

        # Decide whether to reuse the current block as the condition block:
        # reuse if it has no statements (it's an empty connector).
        reuse_as_cond = (len(cur.statements) == 0)

        if reuse_as_cond:
            cond_block = cur
        else:
            cond_block = BasicBlock()
            self.cfg.add_block(cond_block)
            # link cur -> cond_block
            cur.successors.add(cond_block)
            cond_block.predecessors.add(cur)

        # Add the while condition statement into cond_block
        cond_block.add_statement(Statement(
            stmt_type=StatementType.WHILE,
            def_set=set(),
            use_set=set(get_uses(node.test)),
            ast_node=node
        ))

        # Create loop body block
        body_block = BasicBlock()
        self.cfg.add_block(body_block)
        cond_block.successors.add(body_block)
        body_block.predecessors.add(cond_block)

        # Visit the body inside body_block
        self.current_block = body_block
        for stmt in node.body:
            self.visit(stmt)

        # control does not loop back to the condition.
        if not (self.current_block.statements and self.current_block.statements[-1].stmt_type == StatementType.RETURN):
            self.current_block.successors.add(cond_block)
            cond_block.predecessors.add(self.current_block)

        # Create exit block (false branch)
        exit_block = BasicBlock()
        self.cfg.add_block(exit_block)
        cond_block.successors.add(exit_block)
        exit_block.predecessors.add(cond_block)

        # Continue from exit
        self.current_block = exit_block



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
        return set()

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

    return set(uses)

def missing_return(cfg: ControlFlowGraph):
    for block in cfg.blocks:
        for stmt in block.statements:
            if stmt.stmt_type == StatementType.RETURN:
                block.successors.discard(cfg.exit)
                cfg.exit.predecessors.discard(block)
    
    all_cfg_blocks = []
    all_cfg_blocks.append(cfg.entry)
    for block in cfg.blocks:
        all_cfg_blocks.append(block)
    all_cfg_blocks.append(cfg.exit)

    for block in all_cfg_blocks:
        block.in_set = set()
        block.out_set = set()

    all_cfg_blocks[0].in_set = {True}
    
    changed = True
    while changed:
        changed = False
        for bb in all_cfg_blocks:
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
            if bb.in_set != old_in or bb.out_set != old_out:
                changed = True
    
    for bb in cfg.blocks:
        if cfg.exit in bb.successors:
            print(f"{bb.id}: there exists a path to exit without return")

def taint_analysis_statement(statement: Statement, in_set: Set[str], out_set: Set[str]):
    if statement.stmt_type == StatementType.SINK:
        for var in statement.use_set:
            if var in in_set:
                print(f"Tainted data reached sink via variable '{var}'")
    elif statement.stmt_type == StatementType.ASSIGNMENT:
        for var in statement.def_set:
            if var in in_set:
                out_set.add(var)
            else:
                if var in out_set:
                    out_set.remove(var)
    elif statement.stmt_type == StatementType.SOURCE:
        for var in statement.def_set:
            out_set.add(var)


def generate_statement_worklist(cfg: ControlFlowGraph):
    worklist = []
    block_id = 1
    
    # Map to track which worklist items belong to which original block
    # Format: {original_block_id: [(statement_index, worklist_index), ...]}
    block_to_worklist = {}
    
    # First pass: create worklist items for each statement
    for each_block in sorted(cfg.blocks, key=lambda b: b.id):
        if each_block.id == "Entry" or each_block.id == "Exit":
            continue
            
        block_statements = []
        
        for stmt_idx, stmt in enumerate(each_block.statements):
            # Check if this is an assignment from source()
            is_source_assignment = False
            if stmt.stmt_type == StatementType.ASSIGNMENT and stmt.ast_node:
                # Check if the right-hand side is a call to source()
                if isinstance(stmt.ast_node, ast.Assign):
                    if isinstance(stmt.ast_node.value, ast.Call):
                        if isinstance(stmt.ast_node.value.func, ast.Name) and stmt.ast_node.value.func.id == "source":
                            is_source_assignment = True
            
            worklist_item = {
                'block_id': f'BB{block_id}',
                'statement': stmt.stmt_type,
                'original_block_id': each_block.id,
                'stmt_index': stmt_idx,
                'def_set': stmt.def_set.copy(),
                'use_set': stmt.use_set.copy(),
                'is_source_assignment': is_source_assignment,
                'in_set': set(),
                'out_set': set(),
                'predecessors': set(),
                'successors': set()
            }
            worklist.append(worklist_item)
            block_statements.append((stmt_idx, len(worklist) - 1))
            block_id += 1
        
        block_to_worklist[each_block.id] = block_statements
    
    # Second pass: set up predecessors and successors
    for each_block in cfg.blocks:
        if each_block.id == "Entry" or each_block.id == "Exit":
            continue
        
        if each_block.id not in block_to_worklist or not block_to_worklist[each_block.id]:
            continue
        
        block_worklist_items = block_to_worklist[each_block.id]
        num_stmts = len(block_worklist_items)
        
        for i, (stmt_idx, worklist_idx) in enumerate(block_worklist_items):
            current_item = worklist[worklist_idx]
            
            # Set predecessors
            if i == 0:
                # First statement: predecessors are the last statements of predecessor blocks
                for pred_block in each_block.predecessors:
                    if pred_block.id == "Entry":
                        # If predecessor is Entry, this is the first statement of the CFG
                        # Add Entry as a special predecessor (or skip if you want)
                        continue
                    elif pred_block.id in block_to_worklist and block_to_worklist[pred_block.id]:
                        # Add the last statement of the predecessor block
                        last_stmt_worklist_idx = block_to_worklist[pred_block.id][-1][1]
                        current_item['predecessors'].add(worklist[last_stmt_worklist_idx]['block_id'])
            else:
                # Middle statements: predecessor is the previous statement in the same block
                prev_worklist_idx = block_worklist_items[i - 1][1]
                current_item['predecessors'].add(worklist[prev_worklist_idx]['block_id'])
            
            # Set successors
            if i == num_stmts - 1:
                # Last statement: successors are the first statements of successor blocks
                for succ_block in each_block.successors:
                    if succ_block.id == "Exit":
                        # If successor is Exit, this is the last statement before exit
                        continue
                    elif succ_block.id in block_to_worklist and block_to_worklist[succ_block.id]:
                        # Add the first statement of the successor block
                        first_stmt_worklist_idx = block_to_worklist[succ_block.id][0][1]
                        current_item['successors'].add(worklist[first_stmt_worklist_idx]['block_id'])
            else:
                # Middle statements: successor is the next statement in the same block
                next_worklist_idx = block_worklist_items[i + 1][1]
                current_item['successors'].add(worklist[next_worklist_idx]['block_id'])
    
    return worklist

def transfer_taint(block, in_set):
    out_set = set(in_set)
    defs = block['def_set']
    uses = block['use_set']
    stmt_type = block['statement']

    if block.get('is_source_assignment', False):
        out_set |= defs
    elif stmt_type == 'assignment':
        defined_var = next(iter(defs)) if defs else None
        if not uses:
            if defined_var:
                out_set.discard(defined_var)
        elif any(v in in_set for v in uses):
            if defined_var:
                out_set.add(defined_var)
        else:
            if defined_var:
                out_set.discard(defined_var)
    elif stmt_type in ('if', 'while'):
        pass

    return out_set

def run_taint_analysis(worklist):
    changed = True
    while changed:
        changed = False
        for block in worklist:
            preds = block['predecessors']
            in_set = set().union(*(b['out_set'] for b in worklist if b['block_id'] in preds))
            block['in_set'] = in_set
            new_out = transfer_taint(block, in_set)
            if new_out != block['out_set']:
                block['out_set'] = new_out
                changed = True

    # --- After convergence: check for tainted sinks ---
    for block in worklist:
        if block['statement'] == 'sink':
            for v in block['use_set']:
                if v in block['in_set']:
                    print(f"{block['block_id']}: tainted variable {v} reaches sink")


def taint_analysis(cfg: ControlFlowGraph):

    worklist = generate_statement_worklist(cfg)

    run_taint_analysis(worklist)
    
    # print("Initial Worklist:")
    # for item in worklist:
    #     print(f"\t{item}")

def dead_store(cfg: ControlFlowGraph):
    # Compute block-level liveness (standard backward dataflow)
    for bb in cfg.blocks:
        bb.in_set = set()
        bb.out_set = set()

    changed = True
    while changed:
        changed = False
        for bb in cfg.blocks:
            old_in = bb.in_set.copy()
            old_out = bb.out_set.copy()

            new_out = set()
            for succ in bb.successors:
                new_out |= getattr(succ, 'in_set', set())
            bb.out_set = new_out

            bb.in_set = bb.use_set | (bb.out_set - bb.def_set)

            if bb.in_set != old_in or bb.out_set != old_out:
                changed = True
    for bb in sorted(cfg.blocks, key=lambda b: getattr(b, 'id', '')):
        if bb.id in ("Entry", "Exit"):
            continue

        live = set(bb.out_set)
        dead_stores = set()

        for stmt in reversed(bb.statements):
            if stmt.stmt_type == StatementType.ASSIGNMENT:
                for d in stmt.def_set:
                    if d not in live:
                        dead_stores.add(d)

            live -= set(stmt.def_set)
            live |= set(stmt.use_set)
        
        for ds in dead_stores:
            print(f"{bb.id}: variable {ds} definition is never used")

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
    tree = ast.parse(open(fname).read(), filename=fname)
    my_cfg = make_cfg_manager(tree)
    dead_store(my_cfg)
    return -1

# Exercise 2
def do_returns(fname):
    #print("RETURNS not implemented")
    tree = ast.parse(open(fname).read(), filename=fname)
    my_cfg = make_cfg_manager(tree)

    missing_return(my_cfg)
    return -1

# Exercise 3
def do_taints(fname):
    # print("TAINTS not implemented")
    tree = ast.parse(open(fname).read(), filename=fname)
    # print(ast.dump(tree, indent=4))
    my_cfg = make_cfg_manager(tree)
    #my_cfg.cfg_print()

    # Perform taint analysis
    taint_analysis(my_cfg)
    return -1


if __name__ == "__main__":
    main()
