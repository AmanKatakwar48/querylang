# QueryLang_Final: Comprehensive Directory Index & Master Component Guide

**Course:** BCSE307P — Compiler Design Laboratory  
**Project:** QueryLang — Compiler-Style Query Processing Engine with Rule-Based Query Optimization  
**Student:** Aman Katakwar (Registration Number: `24BCE0160`)  
**Faculty Guide:** Prof. Ranjithkumar S  
**Location:** `c:\Users\amank\OneDrive\Desktop\QueryLang_Final`  

---

## 1. Directory Structure & File Map

```text
QueryLang_Final/
│
├── [PDF Deliverables]
│   ├── QueryLang_Review3_Report.pdf        # Final Project Review Academic Report (21 Chapters, A4)
│   ├── QueryLang_Review3_compiler.pdf      # Final Viva Presentation Slides (16:9 Aspect Ratio)
│   ├── QueryLang_Review2_Report.pdf        # Review 2 Academic Progress Report
│   └── QueryLang_Review2_compiler.pdf      # Review 2 Presentation Slides
│
├── [Documentation / Markdown]
│   ├── README.md                           # Master Project Guide & Architecture Overview
│   ├── INDEX.md                            # This component catalog & directory index
│   ├── REVIEW_3_REPORT.md                  # Comprehensive 21-Chapter Review 3 Report
│   ├── REVIEW_3_PRESENTATION.md            # Complete 16-Slide Review 3 Viva Presentation
│   ├── REVIEW_2_REPORT.md                  # Review 2 Formal Academic Report
│   └── REVIEW_2_PRESENTATION.md            # Review 2 Viva Presentation
│
├── [Visualizations]
│   ├── querylang_ast.dot                   # Graphviz DOT file for Abstract Syntax Tree
│   └── querylang_plan.dot                  # Graphviz DOT file for Relational Execution Plan
│
├── [Executable Scripts & CLI Drivers]
│   ├── run.bat                             # Windows one-click batch launcher
│   ├── main.py                             # Interactive REPL, CLI parser, and compiler driver
│   ├── demo_review3.py                     # Review 3 (Final) 6-part live viva demo script
│   ├── demo.py                             # Review 2 live demonstration script
│   ├── all_in_one_querylang.py             # Monolithic single-file standalone compiler build
│   ├── build_review3_pdfs.py               # Automated PDF build engine using headless Edge
│   └── build_pdfs.py                       # Review 2 PDF generation script
│
├── [Subdirectories]
│   ├── PDFs/                               # Dedicated folder containing all 4 compiled PDF documents
│   ├── Documentation/                      # Dedicated folder containing all 5 Markdown specifications
│   ├── Visualizations/                     # Dedicated folder containing Graphviz DOT exports
│   ├── querylang/                          # Modular 6-phase compiler package
│   └── tests/                              # Formal 25-point verification matrix and PyUnit suites
```

---

## 2. Categorized File Manifest

### A. PDF Deliverables (Available at Root and in `PDFs/`)
1. **`QueryLang_Review3_Report.pdf`** (609 KB):  
   Comprehensive, 21-chapter academic project report strictly conforming to the guidelines of Chapter 24 of the Compiler Design Laboratory manual. Includes formal EBNF grammar, architectural flow diagrams, AST hierarchy specifications, semantic typing rules, optimizer algebraic proofs, benchmark speedup data tables, and the complete 25-test verification matrix.
2. **`QueryLang_Review3_compiler.pdf`** (373 KB):  
   High-definition, 16-slide presentation deck designed for final viva defense in 16:9 widescreen format with clear visual contrast, syntax-highlighted code blocks, before/after optimizer comparisons, and performance benchmark tables.
3. **`QueryLang_Review2_Report.pdf`** (330 KB):  
   Formal academic progress report submitted for Review 2 evaluating the core front-end implementation.
4. **`QueryLang_Review2_compiler.pdf`** (333 KB):  
   Presentation slide deck for Review 2 defense.

### B. Documentation (Available at Root and in `Documentation/`)
1. **`REVIEW_3_REPORT.md`**: Complete Markdown source for the 21-chapter final academic report.
2. **`REVIEW_3_PRESENTATION.md`**: Complete Markdown source for the 16-slide viva presentation.
3. **`REVIEW_2_REPORT.md`**: Markdown source for Review 2 report.
4. **`REVIEW_2_PRESENTATION.md`**: Markdown source for Review 2 presentation.
5. **`README.md`**: Project quickstart, installation instructions, and architecture overview.

### C. Compiler Source Code (`querylang/`)
1. **`pipeline.py`**: The central compiler orchestrator executing all 6 phases: Lexer $\to$ Parser $\to$ Semantic Analyzer $\to$ Planner $\to$ Optimizer $\to$ Execution Engine.
2. **`optimizer/`**:
   - `optimizer.py`: Rule-based query optimizer implementing `ConstantFolder`, `PredicateSimplifier`, and `FilterPushdown`.
   - `__init__.py`: Package export interface.
3. **`execution/`**:
   - `engine.py`: In-memory query execution engine interpreting relational algebra operator trees with multi-table inner joins and aggregations.
   - `operators.py`: Evaluates AST expression predicates, comparisons, arithmetic, and qualified attributes.
4. **`planner/`**:
   - `planner.py`: Query plan generator translating validated ASTs to relational algebra IR.
   - `plan.py`: Strongly typed IR plan node definitions (`ScanNode`, `JoinPlanNode`, `FilterNode`, `ProjectNode`, `AggregatePlanNode`, `SortNode`, `LimitNode`).
5. **`semantic/`**:
   - `analyzer.py`: Validates table and column references, resolves multi-table schemas, and checks join conditions.
   - `type_checker.py`: Static type checker verifying comparisons and arithmetic compatibility.
6. **`schema/`**:
   - `catalog.py`: Schema catalog acting as the compiler's symbol table repository.
7. **`parser/`**:
   - `parser.py`: Deterministic LL(1) recursive-descent parser.
   - `grammar.py`: Formal EBNF grammar specification with 6-tier operator precedence.
8. **`ast/`**:
   - `nodes.py`: Strongly typed AST nodes with ASCII tree visualization.
9. **`lexer/`**:
   - `lexer.py`: Deterministic regular-expression scanner with line/column tracking.
   - `tokens.py`: Token classes and `TokenType` enumeration.
10. **`visualization/`**:
    - `visualizer.py`: Graphviz DOT exporter generating graphical trees for ASTs and relational plans.
11. **`benchmarks/`**:
    - `benchmark.py`: Synthetic dataset generator and benchmark runner for 100, 1k, and 10k rows.
12. **`data/`**:
    - `sample_data.py`: Default in-memory relational tables (`students` and `departments`).
13. **`errors/`**:
    - `errors.py`: Compiler exception hierarchy (`LexicalError`, `SyntaxError`, `SemanticError`, `ExecutionError`) with source visual caret pointers.

### D. Test Suites (`tests/`)
1. **`run_all_tests.py`**: Master test runner executing the 25-point formal verification matrix (**T-01 to T-25**) and all PyUnit suites (100% pass rate).
2. **`test_optimizer.py`**: Unit tests for constant folding, predicate simplification, filter pushdown, relational joins, and aggregations.
3. **`test_execution.py`**: Unit tests for physical operators, compound logic, sorting, and limits.
4. **`test_semantic.py`**: Unit tests for symbol table binding, non-existent columns, and type mismatches.
5. **`test_planner.py`**: Unit tests for relational algebra IR plan generation.
6. **`test_parser.py`**: Unit tests for grammar rules, expressions, and syntax errors.
7. **`test_lexer.py`**: Unit tests for tokenization and lexical error detection.

---

## 3. Quick-Start Execution Guide

From within `c:\Users\amank\OneDrive\Desktop\QueryLang_Final`:

```powershell
# 1. Run the Review 3 6-Part Live Viva Demonstration
.\run.bat --review3

# 2. Run the 25-Point Formal Verification Test Suite
.\run.bat --test

# 3. Run the Scale Benchmarking Suite (100, 1k, 10k rows)
.\run.bat --benchmark

# 4. Launch the Interactive Query Shell (REPL)
.\run.bat

# 5. Recompile PDFs from Markdown
python build_review3_pdfs.py
```

---

## 4. Verification Status Summary

- **Formal Verification Matrix:** 25 / 25 Passed (100% Pass Rate).
- **Automated PyUnit Unit Tests:** 26 / 26 Passed (0 Errors, 0 Failures).
- **Empirical Optimization Speedup:** 1.89x (100 rows) to 2.28x (10,000 rows).
- **Join Comparisons Saved:** 73.3% reduction via algebraic filter pushdown.
- **Compiler Independence:** Pure Python Standard Library (Zero external dependencies).
