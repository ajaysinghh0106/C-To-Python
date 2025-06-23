from parser import parse_c_code
from translator import translate_ast_to_python
from translator import translate_ast_to_java
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <c_file_path>")
        sys.exit(1)

    c_file_path = sys.argv[1]
    
    # Interactive menu for language selection
    print("\nSelect target language for conversion:")
    print("1. Python")
    print("2. Java")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    target_java = choice == "2"
    with open(c_file_path, 'r') as f:
        c_code = f.read()

    ast = parse_c_code(c_code)
    
    # Choose translator based on target language
    if target_java:
        generated_code = translate_ast_to_java(ast)
        output_file = "translated.java"
    else:
        generated_code = translate_ast_to_python(ast)
        output_file = "translated.py"

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    output_path = os.path.join("output", output_file)
    with open(output_path, 'w') as f:
        f.write(generated_code)

    print(f"Translation complete. Output saved to {output_path}")

if __name__ == "__main__":
    main()
