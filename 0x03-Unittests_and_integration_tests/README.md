# 0x03 - Unittests and Integration Tests

This project focuses on writing unit and integration tests in Python using the `unittest` framework and the `parameterized` library. The goal is to ensure reliability, maintainability, and correctness of utility functions used within a GitHub organization client.

## Project Structure

- **utils.py**  
  Contains generic utility functions:
  - `access_nested_map()`: Safely access values inside nested dictionaries.
  - `get_json()`: Retrieve JSON content from a URL.
  - `memoize()`: Decorator that caches method results.

- **test_utils.py**  
  Unit tests for functions in `utils.py`, particularly `access_nested_map`, using `unittest` and `parameterized.expand`.

## Features

- Follows `pycodestyle` 2.5 for clean and readable code.
- All files start with `#!/usr/bin/env python3` and are executable.
- All modules, classes, and functions are documented with real, meaningful docstrings.
- All functions and methods are type-annotated for better readability and static analysis support.

## How to Run Tests

Make sure `parameterized` is installed:
```bash
pip install parameterized
