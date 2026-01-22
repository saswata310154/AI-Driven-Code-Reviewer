import ast

class ErrorFinder(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.defined_vars = set()
        self.used_vars = set()
        self.defined_imports = set()

    def visit_Assign(self, node):
        """When we see: x = 5"""    
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        """Capture: import requests"""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.defined_imports.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Capture: from requests import get"""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.defined_imports.add(name)
        self.generic_visit(node)

    def visit_Name(self, node):
        """Capture any time a name is loaded (used)"""
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        self.generic_visit(node)

    def find_unused_variables(self):
        unused = self.defined_vars - self.used_vars
        for var in unused:
            self.errors.append({
                "type": "UnusedVariable",
                "message": f"Variable '{var}' is defined but never used",
                "suggestion": f"Remove '{var}' or use it in your code"
            })
        return self.errors

    def find_unused_imports(self):
        """Check for imports that were never referenced"""
        unused = self.defined_imports - self.used_vars
        for imp in unused:
            self.errors.append({
                "type": "UnusedImport",
                "message": f"Import '{imp}' is unused",
                "suggestion": f"Remove 'import {imp}' to clean up your code"
            })
        return self.errors

def detect_errors(code_string):
    try:
        tree = ast.parse(code_string)
        finder = ErrorFinder()
        finder.visit(tree)

        # Run both checks
        finder.find_unused_variables()
        finder.find_unused_imports()

        return {
            "success": True,
            "errors": finder.errors,
            "error_count": len(finder.errors)
        }
    except SyntaxError as e:
        return {"success": False, "error": str(e)}