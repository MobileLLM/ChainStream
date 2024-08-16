import importlib.util
import ast

def extract_imports(code: str):
    tree = ast.parse(code)
    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imported_modules.add(node.module)

    return list(imported_modules)

def check_library_installed(library_names: list) -> bool:
    for library in library_names:
        if not check_library_installed_single(library):
            raise ImportError(f"{library} is not installed.")
    return True

