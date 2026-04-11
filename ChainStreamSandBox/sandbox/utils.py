import importlib.util
import ast
import re


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
        if not importlib.util.find_spec(library):
            raise ImportError(f"{library} is not installed.")
    return True


def escape_string_literals(text):
    # 正则表达式用于匹配双引号或单引号之间的内容，包括多个 \n 的情况
    pattern = r'(["\'])(.*?)(?<!\\)(\\n)(.*?)(?<!\\)(["\'])'

    # 替换所有在引号内的 \n 为 \\n
    modified_text = re.sub(pattern, lambda m: m.group(1) + m.group(2).replace('\n', '【换行符】') + m.group(4) + m.group(5), text, flags=re.DOTALL)
    return modified_text

if __name__ == '__main__':
    # 示例
    input_text = '''这是一个例子:
    "This is a test
    with new line."
    还有一个例子:
    'Another test
    with new line and
    another line.'
    单个换行符也会被替换: "Single
    newline." 
    '''
    output_text = escape_string_literals(input_text)
    print(output_text)
