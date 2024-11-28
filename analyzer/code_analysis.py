import ast
import json
import os

def parse_code(file_path):
    with open(file_path, "r") as file:
        code = file.read()
    return ast.parse(code)

def is_spaghetti_code(node):
    if isinstance(node, ast.FunctionDef):
        complexity = sum(isinstance(n, (ast.If, ast.For, ast.While, ast.Try)) for n in ast.walk(node))
        return complexity > 10  # Complexity threshold
    return False

def is_golden_hammer(node):
    if isinstance(node, ast.Import):
        imported_libs = [alias.name for alias in node.names]
        return len(set(imported_libs)) == 1 and imported_libs[0] in ('requests', 'numpy')
    return False

def is_boat_anchor(node, all_names):
    if isinstance(node, ast.Import):
        for alias in node.names:
            if alias.name not in all_names:
                return True  # Import not used
    return False

def is_dead_code(node):
    if isinstance(node, ast.FunctionDef):
        found_return = False
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                found_return = True
            elif found_return:
                return True  # Code following return is dead
    return False

def is_god_object(node):
    if isinstance(node, ast.ClassDef):
        method_count = sum(isinstance(n, ast.FunctionDef) for n in node.body)
        return method_count > 10  # Threshold for too many methods
    return False

class AntiPatternVisitor(ast.NodeVisitor):
    def __init__(self):
        self.report = []
        self.all_names = set()

    def visit_FunctionDef(self, node):
        if is_spaghetti_code(node):
            self.report.append({"type": "Spaghetti Code", "line": node.lineno, "message": "High cyclomatic complexity"})
        if is_dead_code(node):
            self.report.append({"type": "Dead Code", "line": node.lineno, "message": "Unreachable code detected"})
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if is_god_object(node):
            self.report.append({"type": "God Object", "line": node.lineno, "message": "Class with too many responsibilities"})
        self.generic_visit(node)

    def visit_Import(self, node):
        if is_golden_hammer(node):
            self.report.append({"type": "Golden Hammer", "line": node.lineno, "message": "Single library heavily relied upon"})
        if is_boat_anchor(node, self.all_names):
            self.report.append({"type": "Boat Anchor", "line": node.lineno, "message": "Unused import"})
        self.generic_visit(node)

    def visit_Name(self, node):
        self.all_names.add(node.id)
        self.generic_visit(node)

def analyze_folder(folder_path):
    reports = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                tree = parse_code(full_path)
                visitor = AntiPatternVisitor()
                visitor.visit(tree)
                for item in visitor.report:
                    item["file"] = full_path
                    reports.append(item)
    return reports
