from pycparser.c_ast import *

def translate_ast_to_python(ast):
    python_lines = []

    def visit(node, indent=0):
        ind = "    " * indent
        if isinstance(node, FileAST):
            for ext in node.ext:
                visit(ext, indent)
        elif isinstance(node, FuncDef):
            name = node.decl.name
            args = []
            if node.decl.type.args:
                args = [param.name for param in node.decl.type.args.params]
            python_lines.append(f"{ind}def {name}({', '.join(args)}):")
            visit(node.body, indent + 1)
        elif isinstance(node, Compound):
            for stmt in node.block_items or []:
                visit(stmt, indent)
        elif isinstance(node, Decl) and isinstance(node.type, TypeDecl):
            if node.init:
                python_lines.append(f"{ind}{node.name} = {translate_expr(node.init)}")
            else:
                python_lines.append(f"{ind}{node.name} = None")
        elif isinstance(node, Assignment):
            lval = node.lvalue.name
            rval = translate_expr(node.rvalue)
            python_lines.append(f"{ind}{lval} = {rval}")
        elif isinstance(node, If):
            cond = translate_expr(node.cond)
            python_lines.append(f"{ind}if {cond}:")
            visit(node.iftrue, indent + 1)
            if node.iffalse:
                python_lines.append(f"{ind}else:")
                visit(node.iffalse, indent + 1)
        elif isinstance(node, For):
            if isinstance(node.init, Assignment):
                init = node.init.lvalue.name
                start = translate_expr(node.init.rvalue)
            else:
                init = "i"
                start = "0"
            if isinstance(node.cond, BinaryOp):
                end = translate_expr(node.cond.right)
            else:
                end = "10"
            python_lines.append(f"{ind}for {init} in range({start}, {end}):")
            visit(node.stmt, indent + 1)
        elif isinstance(node, Return):
            python_lines.append(f"{ind}return {translate_expr(node.expr)}")

    def translate_expr(expr):
        if isinstance(expr, Constant):
            return expr.value
        elif isinstance(expr, ID):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = translate_expr(expr.left)
            right = translate_expr(expr.right)
            return f"{left} {expr.op} {right}"
        return "None"

    visit(ast)
    return "\n".join(python_lines)

def translate_ast_to_java(ast):
    java_lines = []
    current_function = [None]  # Track current function name
    
    def get_java_type(type_name):
        # Map C types to Java types
        type_map = {
            'int': 'int',
            'float': 'float',
            'double': 'double',
            'char': 'char',
            'void': 'void',
            '_Bool': 'boolean'
        }
        return type_map.get(type_name, 'Object')

    def visit(node, indent=0):
        ind = "    " * indent
        if isinstance(node, FileAST):
            java_lines.append("class Program {")
            for ext in node.ext:
                visit(ext, indent + 1)
            java_lines.append("}")
        elif isinstance(node, FuncDef):
            name = node.decl.name
            current_function[0] = name
            return_type = get_java_type(node.decl.type.type.type.names[0])
            args = []
            if node.decl.type.args:
                for param in node.decl.type.args.params:
                    param_type = get_java_type(param.type.type.names[0])
                    args.append(f"{param_type} {param.name}")
            modifier = "public static"
            if name == "main":
                java_lines.append(f"{ind}{modifier} void {name}(String[] args) {{")
            else:
                java_lines.append(f"{ind}{modifier} {return_type} {name}({', '.join(args)}) {{")
            visit(node.body, indent + 1)
            java_lines.append(f"{ind}}}")
            current_function[0] = None
        elif isinstance(node, Compound):
            for stmt in node.block_items or []:
                visit(stmt, indent)
        elif isinstance(node, Decl) and isinstance(node.type, TypeDecl):
            type_name = get_java_type(node.type.type.names[0])
            if node.init:
                java_lines.append(f"{ind}{type_name} {node.name} = {translate_expr(node.init)};")
            else:
                java_lines.append(f"{ind}{type_name} {node.name};")
        elif isinstance(node, Assignment):
            lval = node.lvalue.name
            rval = translate_expr(node.rvalue)
            java_lines.append(f"{ind}{lval} = {rval};")
        elif isinstance(node, If):
            cond = translate_expr(node.cond)
            java_lines.append(f"{ind}if ({cond}) {{")
            visit(node.iftrue, indent + 1)
            java_lines.append(f"{ind}}}")
            if node.iffalse:
                java_lines.append(f"{ind}else {{")
                visit(node.iffalse, indent + 1)
                java_lines.append(f"{ind}}}")
        elif isinstance(node, For):
            if isinstance(node.init, Assignment):
                init = f"{node.init.lvalue.name} = {translate_expr(node.init.rvalue)}"
            else:
                init = "int i = 0"
            if isinstance(node.cond, BinaryOp):
                cond = translate_expr(node.cond)
            else:
                cond = "i < 10"
            if hasattr(node, 'next') and isinstance(node.next, Assignment):
                step = f"{node.next.lvalue.name} {node.next.op} {translate_expr(node.next.rvalue)}"
            else:
                step = "i++"
            java_lines.append(f"{ind}for ({init}; {cond}; {step}) {{")
            visit(node.stmt, indent + 1)
            java_lines.append(f"{ind}}}")
        elif isinstance(node, Return):
            if current_function[0] == "main":
                if node.expr:
                    java_lines.append(f'{ind}System.out.println({translate_expr(node.expr)});')
                # Do not emit any return in main
            elif node.expr:
                java_lines.append(f"{ind}return {translate_expr(node.expr)};")
            else:
                java_lines.append(f"{ind}return;")

    def translate_expr(expr):
        if isinstance(expr, Constant):
            # Handle boolean literals
            if expr.value.lower() == 'true' or expr.value.lower() == 'false':
                return expr.value.lower()
            return expr.value
        elif isinstance(expr, ID):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = translate_expr(expr.left)
            right = translate_expr(expr.right)
            # Convert C operators to Java operators if needed
            op_map = {
                '&&': '&&',
                '||': '||',
                '==': '==',
                '!=': '!=',
                '<': '<',
                '>': '>',
                '<=': '<=',
                '>=': '>=',
                '+': '+',
                '-': '-',
                '*': '*',
                '/': '/'
            }
            op = op_map.get(expr.op, expr.op)
            return f"{left} {op} {right}"
        elif isinstance(expr, FuncCall):
            name = expr.name.name
            args = []
            if expr.args:
                for arg in expr.args.exprs:
                    args.append(translate_expr(arg))
            return f"{name}({', '.join(args)})"
        return "null"

    visit(ast)
    return "\n".join(java_lines)
