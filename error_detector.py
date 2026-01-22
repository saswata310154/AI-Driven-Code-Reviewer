import ast


class StaticIssueAnalyzer(ast.NodeVisitor):
    """
    Performs static analysis on Python AST to detect:
    - Unused variables
    - Unused imports
    """

    def __init__(self):
        self.issues = []
        self.declared_vars = set()
        self.used_identifiers = set()
        self.imported_symbols = set()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.declared_vars.add(target.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imported_symbols.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imported_symbols.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_identifiers.add(node.id)
        self.generic_visit(node)

    def collect_unused_variables(self):
        for var in self.declared_vars - self.used_identifiers:
            self.issues.append({
                "type": "UnusedVariable",
                "message": f"Variable '{var}' is defined but never used",
                "suggestion": f"Remove '{var}' or reference it in your code"
            })

    def collect_unused_imports(self):
        for imp in self.imported_symbols - self.used_identifiers:
            self.issues.append({
                "type": "UnusedImport",
                "message": f"Imported module '{imp}' is not used",
                "suggestion": f"Delete the unused import '{imp}'"
            })


def detect_errors(code_string: str):
    """
    Entry point for static error detection.
    Called directly from the Streamlit app.
    """
    try:
        syntax_tree = ast.parse(code_string)
        analyzer = StaticIssueAnalyzer()
        analyzer.visit(syntax_tree)

        analyzer.collect_unused_variables()
        analyzer.collect_unused_imports()

        return {
            "success": True,
            "errors": analyzer.issues,
            "error_count": len(analyzer.issues)
        }

    except SyntaxError as exc:
        return {
            "success": False,
            "error": str(exc)
        }
