# QueryLang: A Compiler-Style Query Processing Engine
**Faculty Guide:** Prof. Ranjithkumar S  
---

## 1. Project Overview

**QueryLang** is an educational, compiler-inspired query processing engine for a restricted SQL-like domain-specific language (DSL). Rather than treating query processing as a black-box database engine, QueryLang models each stage of relational query evaluation using classical **Compiler Design** principles and data structures:

$$\text{Source Query} \xrightarrow{\text{Lexer}} \text{Tokens} \xrightarrow{\text{Parser}} \text{AST} \xrightarrow{\text{Semantic Analyzer}} \text{Decorated AST} \xrightarrow{\text{Planner}} \text{Logical Plan (IR)} \xrightarrow{\text{Engine}} \text{Result}$$

---

## 2. Review 2 Implementation Status

All mandatory Phase 2 deliverables specified in the Project Instruction Manual and Roadmap have been fully implemented, validated, and verified:

| Component | Status | Description |
|---|---|---|
| **Lexical Analyzer** | **Complete** | Tokenizes keywords, identifiers, strings, ints, floats, booleans, operators, and comments. Reports exact `(line, col)` lexical errors. |
| **Parser & CFG** | **Complete** | Recursive-descent LL(1) parser implementing formal EBNF grammar with operator precedence. |
| **Abstract Syntax Tree (AST)** | **Complete** | Type-safe AST nodes (`SelectQueryNode`, `BinaryOpNode`, `ColumnNode`, `LiteralNode`, etc.) with ASCII tree visualizer. |
| **Symbol Table (Schema Catalog)** | **Complete** | Manages relational schemas (`students`, `departments`), data types, and attribute metadata. |
| **Semantic Analyzer & Type Checker** | **Complete** | Validates table and column identifiers against the catalog; statically checks operator type compatibility. |
| **Query Planner (IR Generator)** | **Complete** | Emits relational algebra Intermediate Representation tree (`SCAN`, `FILTER`, `PROJECT`, `SORT`, `LIMIT`). |
| **In-Memory Execution Engine** | **Complete** | Interprets IR execution plan over in-memory datasets with predicate evaluation and formatted tabular output. |
| **Diagnostics & Error Recovery** | **Complete** | Precise context-aware errors (`LexicalError`, `SyntaxError`, `SemanticError`, `ExecutionError`) with source visual indicators (`^`). |
| **Automated Test Suite** | **Complete** | 16-test formal verification matrix + 20 PyUnit test cases (100% pass rate). |
| **Interactive CLI & REPL** | **Complete** | Multi-mode driver supporting single queries, file execution, interactive shell, symbol table dump, and stage inspections. |

---

## 3. Directory Structure

```text
QueryLang/
│
├── querylang/                     # Core Compiler Package
│   ├── errors/
│   │   ├── __init__.py
│   │   └── errors.py              # Specialized diagnostic error hierarchy
│   ├── lexer/
│   │   ├── __init__.py
│   │   ├── tokens.py              # Token and TokenType enum definitions
│   │   └── lexer.py               # Regex-based deterministic lexical analyzer
│   ├── ast/
│   │   ├── __init__.py
│   │   └── nodes.py               # AST node classes and ASCII tree visualizer
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── grammar.py             # EBNF grammar specification & documentation
│   │   └── parser.py              # Recursive-descent predictive parser
│   ├── schema/
│   │   ├── __init__.py
│   │   └── catalog.py             # Symbol Table / Schema Catalog repository
│   ├── semantic/
│   │   ├── __init__.py
│   │   ├── type_checker.py        # Static type checking rules
│   │   └── analyzer.py            # Scope checker & semantic validator
│   ├── planner/
│   │   ├── __init__.py
│   │   ├── plan.py                # Intermediate Representation (IR) plan nodes
│   │   └── planner.py             # Relational query plan generator
│   ├── execution/
│   │   ├── __init__.py
│   │   ├── operators.py           # In-memory predicate evaluator
│   │   └── engine.py              # Execution engine & formatted table printer
│   ├── data/
│   │   ├── __init__.py
│   │   └── sample_data.py         # In-memory test datasets (students, departments)
│   ├── __init__.py
│   └── pipeline.py                # Unified compiler pipeline orchestrator
│
├── tests/                         # Test Suite
│   ├── test_lexer.py              # Lexical unit tests
│   ├── test_parser.py             # Syntactic & AST unit tests
│   ├── test_semantic.py           # Semantic validation & type checking tests
│   ├── test_planner.py            # IR query plan generator tests
│   ├── test_execution.py          # Execution engine tests
│   └── run_all_tests.py           # Comprehensive 16-test formal verification runner
│
├── demo.py                        # Review 2 official demonstration script
├── main.py                        # Interactive shell & CLI compiler driver
├── run.bat                        # Windows launch script
└── README.md                      # Project manual and documentation
```

---

## 4. How to Run the Prototype

All scripts can be executed using Python 3:

### Option A: Using Windows Batch Script
```cmd
cd c:\Users\amank\OneDrive\Desktop\QueryLang

# Run the 5 official Review 2 Demos:
run.bat --demo

# Run the 16-test formal verification matrix:
run.bat --test

# Launch the Interactive QueryLang Shell:
run.bat
```

### Option B: Using Python Directly
```bash
# Execute a single query with stage-by-stage compiler inspection:
python main.py -q "SELECT name, cgpa FROM students WHERE cgpa >= 8.5 AND age > 20;" -i

# Inspect the Symbol Table / Schema Catalog:
python main.py --schema

# Run the live demonstration:
python demo.py

# Run all unit tests:
python tests/run_all_tests.py
```

---

## 5. Review 2 Demonstration Summary

The project includes pre-configured test cases matching the five canonical demos required by Review 2:

1. **Demo 1: Basic SELECT Projection**  
   `SELECT name FROM students;`  
   *Demonstrates:* Clean lexical scan, parse tree, column projection, and tabular output.
2. **Demo 2: Filtered Query with Relational Predicate**  
   `SELECT name, age, cgpa FROM students WHERE age > 20;`  
   *Demonstrates:* AST condition parsing, intermediate `FILTER` node execution.
3. **Demo 3: Semantic Error Detection**  
   - `SELECT salary FROM students;` $\rightarrow$ Catches undeclared column; lists available table columns.  
   - `SELECT name FROM students WHERE name > 50;` $\rightarrow$ Catches type incompatibility (`STRING` vs `INTEGER`).
4. **Demo 4: Syntactic Error Detection**  
   - `SELECT FROM students;` $\rightarrow$ Parser identifies missing projection column list.  
   - `SELECT name students;` $\rightarrow$ Parser identifies missing `FROM` keyword.
5. **Demo 5: Deep-Dive Stage-by-Stage Compiler Inspection**  
   Inspects Token stream $\rightarrow$ AST hierarchy $\rightarrow$ Symbol Table resolution $\rightarrow$ Relational Algebra IR $\rightarrow$ Final table.
