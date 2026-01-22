import ast


class StaticIssueDetector(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.assigned_names = set()
        self.referenced_names = set()
        self.imported_items = set()

    def visit_Assign(self, node):
        # Track variables on the left-hand side of assignments
        for item in node.targets:
            if isinstance(item, ast.Name):
                self.assigned_names.add(item.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        # Handle: import module / import module as alias
        for entry in node.names:
            identifier = entry.asname if entry.asname else entry.name
            self.imported_items.add(identifier)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Handle: from module import name / name as alias
        for entry in node.names:
            identifier = entry.asname if entry.asname else entry.name
            self.imported_items.add(identifier)
        self.generic_visit(node)

    def visit_Name(self, node):
        # Record every variable that is read/used
        if isinstance(node.ctx, ast.Load):
            self.referenced_names.add(node.id)
        self.generic_visit(node)

    def report_unused_variables(self):
        unused_vars = self.assigned_names - self.referenced_names
        for name in unused_vars:
            self.issues.append({
                "type": "UnusedVariable",
                "message": f"Variable '{name}' is defined but never used",
                "suggestion": f"Either remove '{name}' or reference it somewhere in the code"
            })

    def report_unused_imports(self):
        unused_imports = self.imported_items - self.referenced_names
        for name in unused_imports:
            self.issues.append({
                "type": "UnusedImport",
                "message": f"Import '{name}' is never used",
                "suggestion": f"Remove 'import {name}' to improve code clarity"
            })


def detect_errors(source_code):
    try:
        syntax_tree = ast.parse(source_code)
        analyzer = StaticIssueDetector()
        analyzer.visit(syntax_tree)

        analyzer.report_unused_variables()
        analyzer.report_unused_imports()

        return {
            "success": True,
            "errors": analyzer.issues,
            "error_count": len(analyzer.issues)
        }

    except SyntaxError as error:
        return {
            "success": False,
            "error": str(error)
        }
