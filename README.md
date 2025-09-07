# DSL Parser

A Python library for parsing Domain-Specific Languages (DSL).

---

## Description

**DSL Parser** is a lightweight, flexible, and extensible Python framework designed to simplify the creation of parsers for custom domain-specific languages.  

It provides:  
- A clear separation between metadata, triggers, and parsed data views.  
- Cursor-based parsing control with support for both text and binary formats.  
- Easy integration of custom callback handlers for specific triggers.  
- An architecture inspired by well-known frameworks (e.g., Qt Model/View), promoting clean and maintainable code.  

Ideal for:  
- Parsing proprietary file formats.  
- Building interpreters for mini-languages or configuration DSLs.  
- Processing streams where metadata and trigger patterns guide parsing logic.

---

## Features

- **Modular design:** Easily extend and customize parsers by inheriting base classes.  
- **Trigger-based parsing:** Define triggers that activate callbacks to process special segments of input data.  
- **Metadata handling:** Support for fixed-length metadata fields that are processed prior to main parsing.  
- **Multiple data views:** Return parsed results in various forms, such as JSON or raw byte views.  
- **Support for both text and binary inputs:** With separate subclasses to handle encoding-specific logic.  
- **Pythonic API:** Use decorators to register triggers and metadata readers cleanly.  

---

## Installation

You can install the package using pip (once published):

```bash
pip install dslparser
```

License

MIT License © 2025 Danila Efimov
