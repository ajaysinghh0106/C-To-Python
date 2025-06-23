from pycparser import c_parser

def preprocess_code(code):
    # Remove lines starting with # (preprocessor directives)
    lines = code.splitlines()
    filtered_lines = [line for line in lines if not line.strip().startswith('#')]
    return "\n".join(filtered_lines)

def parse_c_code(code):
    parser = c_parser.CParser()
    clean_code = preprocess_code(code)
    return parser.parse(clean_code)
