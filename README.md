# Compile - C to Python Converter

## Overview

This tool parses basic C programs and converts them into semantically equivalent Python code using `pycparser`.

## Usage

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Run the converter:
    ```
    python main.py examples/sample.c
    ```

3. Check output in `output/translated.py`

## Supported Features

- Function definitions
- Variable declarations
- Assignments
- If statements
- For loops (basic counting)
- Return statements