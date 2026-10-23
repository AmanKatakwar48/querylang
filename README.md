# QueryLang: A Compiler-Style Query Processing Engine with Rule-Based Query Optimization

**Final Project Review (Review 3) & Complete Implementation Manual**  
**Course:** BCSE307P – Compiler Design Laboratory  
**Academic Year:** 2026–27  
**Student Name:** Aman Katakwar  
**Registration Number:** 24BCE0160  
**Faculty Guide:** Prof. Ranjithkumar S  
**Institution:** School of Computer Science and Engineering, Vellore Institute of Technology  

---

## 1. Project Overview

**QueryLang** is an end-to-end, compiler-style query processing engine for a declarative relational domain-specific language (DSL). Rather than treating relational querying as a simple runtime database interpreter, QueryLang models each stage of query evaluation using classical **Compiler Design** theory, intermediate code generation, and program optimization:

$$\text{Source Query} \xrightarrow{\text{Lexer}} \text{Tokens} \xrightarrow{\text{Parser}} \text{AST} \xrightarrow{\text{Semantic Analyzer}} \text{Validated Query} \xrightarrow{\text{Planner}} \text{Logical Plan (IR)} \xrightarrow{\text{Optimizer}} \text{Optimized Plan} \xrightarrow{\text{Execution Engine}} \text{Tabular Result}$$

QueryLang is developed strictly from first principles using standard **Python 3.12** with zero third-party compiler or database dependencies.

---

## 2. Review 3 Implementation Status & Deliverables

All prescribed milestones for Review 1, Review 2, and Review 3 have been fully achieved, formally verified, and empirically benchmarked:

| Component / Subsystem | Review Milestone | Implementation Status | Technical Highlights |
|---|:---:|:---:|---|
| **Lexical Analyzer** | Review 1 & 2 | **Complete** | Deterministic scanner with 27 token types, line/column coordinate tracking, and visual caret error pointers. |
| **Parser & AST** | Review 2 | **Complete** | LL(1) recursive-descent parser producing strongly typed AST hierarchy conforming to an unambiguous EBNF grammar with a 6-tier operator precedence hierarchy. |
| **Schema Catalog & Symbol Table** | Review 2 & 3 | **Complete** | Multi-schema symbol table repository managing relation schemas (`students`, `departments`), column data types, and cross-schema attribute resolution. |
| **Semantic Analyzer & Type Checker** | Review 2 & 3 | **Complete** | Static type checking for comparisons, arithmetic operators, aggregate compatibility, and multi-table column disambiguation. |
| **Intermediate Representation (IR)** | Review 2 & 3 | **Complete** | Relational algebra intermediate code tree (`SCAN`, `JOIN`, `FILTER`, `PROJECT`, `AGGREGATE`, `SORT`, `LIMIT`). |
| **Rule-Based Query Optimizer** | Review 3 | **Complete** | **Constant Folding:** Static compile-time arithmetic evaluation (`(18 + 2) -> 20`) and comparison folding.<br>**Predicate Simplification:** Boolean identity/annihilation laws ($P \land \text{TRUE} \to P$) and redundant filter elimination.<br>**Filter Pushdown:** Algebraic relocation of selections before joins ($\pi(\sigma(R \bowtie S)) \to \pi(\sigma(R) \bowtie S)$). |
| **Language Extensions** | Review 3 | **Complete** | Multi-table relational `INNER JOIN ... ON ...`, qualified attribute lookups (`students.name`), and scalar aggregations (`COUNT`, `AVG`, `SUM`, `MIN`, `MAX`). |
| **Execution Engine** | Review 2 & 3 | **Complete** | In-memory relational operator walking engine producing formatted, aligned ASCII tables and telemetry. |
| **Graphviz DOT Visualizer** | Review 3 | **Complete** | Generates standard Graphviz DOT files for ASTs, execution plans, and side-by-side Before/After optimization subgraphs. |
| **Empirical Benchmarks** | Review 3 | **Complete** | Synthetic dataset scaling across 100, 1,000, and 10,000 records demonstrating an average **1.89x to 2.28x speedup**. |
| **Verification Test Suite** | Review 2 & 3 | **Complete** | Formal 25-point verification matrix (**T-01 to T-25**) + 26 PyUnit unit tests (**100% Pass Rate**). |
| **Academic Documentation & PDFs** | Review 3 | **Complete** | 21-Chapter Academic Report (`QueryLang_Review3_Report.pdf`) and 16-Slide Viva Presentation (`QueryLang_Review3_compiler.pdf`). |

---

## 3. Directory Layout

```text
QueryLang_Final/
├── README.md                           # Master Project Manual & Quickstart Guide
├── INDEX.md                            # Comprehensive File Directory & Component Index
├── run.bat                             # Windows one-click command-line launcher
├── main.py                             # Interactive CLI & Compiler Driver
├── demo_review3.py                     # Review 3 (Final) 6-part live viva demo script
├── demo.py                             # Review 2 live demonstration script
├── all_in_one_querylang.py             # Single-file monolithic build of the compiler
├── build_review3_pdfs.py               # Review 3 PDF compilation script (headless Edge)
├── build_pdfs.py                       # Review 2 PDF compilation script
│
├── PDFs/                               # Downloadable PDF Deliverables
│   ├── QueryLang_Review3_Report.pdf    # Final 21-Chapter Academic Project Report
│   ├── QueryLang_Review3_compiler.pdf  # Final 16-Slide Viva Defense Presentation
│   ├── QueryLang_Review2_Report.pdf    # Review 2 Academic Progress Report
│   └── QueryLang_Review2_compiler.pdf  # Review 2 Presentation Slides
│
├── Documentation/                      # Markdown Source Documentation
│   ├── REVIEW_3_REPORT.md              # Complete 21-chapter Review 3 academic report
│   ├── REVIEW_3_PRESENTATION.md        # Complete 16-slide Review 3 viva presentation
│   ├── REVIEW_2_REPORT.md              # Review 2 academic report
│   ├── REVIEW_2_PRESENTATION.md        # Review 2 presentation
│   └── README.md                       # Architecture & grammar reference
│
├── Visualizations/                     # Exported Graphviz DOT Visualizer Files
│   ├── querylang_ast.dot               # AST Graphviz Digraph
│   └── querylang_plan.dot              # Execution Plan Graphviz Digraph
│
├── querylang/                          # Modular 6-Phase Compiler Package
│   ├── __init__.py
│   ├── pipeline.py                     # Compiler pipeline driver (inspect & execute)
│   ├── ast/                            # Abstract Syntax Tree nodes & ASCII visualizer
│   ├── benchmarks/                     # Synthetic scaling benchmark suite (100, 1k, 10k rows)
│   ├── data/                           # In-memory sample databases (students, departments)
│   ├── errors/                         # Diagnostic exceptions with source visual pointers
│   ├── execution/                      # Execution engine, operators, and table formatter
│   ├── lexer/                          # Linear token scanner & coordinate tracking
│   ├── optimizer/                      # Rule-based query optimizer (folding, pushdown)
│   ├── parser/                         # LL(1) recursive-descent parser & EBNF grammar
│   ├── planner/                        # Relational algebra logical query plan generator
│   ├── schema/                         # Schema catalog symbol table
│   ├── semantic/                       # Semantic validator & static type checker
│   └── visualization/                  # Graphviz DOT exporter
│
└── tests/                              # Formal Quality Assurance & Unit Tests
    ├── run_all_tests.py                # Formal 25-point verification matrix runner
    ├── test_lexer.py                   # Lexical analyzer unit tests
    ├── test_parser.py                  # Parser & AST unit tests
    ├── test_semantic.py                # Semantic & static type checking unit tests
    ├── test_planner.py                 # Query planner & IR unit tests
    ├── test_optimizer.py               # Optimizer, Join, Aggregate & Arithmetic unit tests
    └── test_execution.py               # Physical execution operator unit tests
```

---

## 4. How to Run & Verify

All commands can be executed using `run.bat` or standard Python 3.12:

### 1. Run the Review 3 Live Viva Demonstration (6 Parts)
```powershell
.\run.bat --review3
# or: python demo_review3.py
```
*Demonstrates: (1) Full Pipeline & Optimization, (2) Relational Joins, (3) Filter Pushdown, (4) Aggregations, (5) Scale Benchmarks, (6) Diagnostics & DOT Visualizer.*

### 2. Run the Formal 25-Point Verification Matrix (T-01 to T-25)
```powershell
.\run.bat --test
# or: python tests\run_all_tests.py
```
*Executes all 25 formal verification tests and 26 PyUnit unit tests with 100% pass rate.*

### 3. Run the Empirical Scale Benchmarking Suite
```powershell
.\run.bat --benchmark
```
*Compares Unoptimized vs. Optimized execution timing across 100, 1,000, and 10,000 synthetic rows.*

### 4. Launch the Interactive Query Shell (REPL)
```powershell
.\run.bat
```
*Interactive commands:*
- `\inspect <query>;` : Shows stage-by-stage tokens, AST, symbol table binding, unoptimized plan, optimizer report, and executed result.
- `\schema` : Displays active catalog symbol table.
- `\dot <query>;` : Exports Graphviz DOT files for AST and query plan.
- `\demo` : Runs Review 3 demonstration suite.
- `\benchmark` : Runs scale benchmarks.
- `\test` : Runs verification test suite.
- `\quit` : Exits shell.

### 5. Recompile PDFs from Markdown / HTML
```powershell
python build_review3_pdfs.py
```
*Regenerates `QueryLang_Review3_compiler.pdf` and `QueryLang_Review3_Report.pdf` using headless Microsoft Edge.*
