# REVIEW – 2 PRESENTATION SLIDES
## QueryLang: A Compiler-Style Query Processing Engine
### Phase 2 — Core Implementation Review

**Course:** BCSE307P – Compiler Design  
**Student Name:** Aman Katakwar  
**Reg. No.:** 24BCE0160  
**Submitted to:** Prof. Ranjithkumar S  
**Academic Year:** 2026–2027  

---

### SLIDE 1: Title Slide
- **Title:** REVIEW – 2: QueryLang: A Compiler-Style Query Processing Engine
- **Subtitle:** Phase 2 — Core Implementation & Functional Prototype
- **Course Code:** BCSE307P (Compiler Design Laboratory)
- **Student Details:** Aman Katakwar (Reg. No.: 24BCE0160)
- **Faculty Guide:** Prof. Ranjithkumar S
- **Milestone Focus:** End-to-End Compiler Pipeline: Lexer $\rightarrow$ Parser $\rightarrow$ AST $\rightarrow$ Symbol Table $\rightarrow$ Semantic Analyzer $\rightarrow$ Query Planner (IR) $\rightarrow$ Execution Engine

---

### SLIDE 2: Evolution from Review 1 to Review 2
- **Review 1 Status (Proposal & Design):**
  - Problem definition and formal EBNF grammar defined.
  - Multi-stage architecture established.
  - Initial proof-of-concept Python Lexer prototype.
- **Review 2 Milestone (Core Implementation):**
  - Completed hand-written Recursive-Descent Parser.
  - Constructed type-safe Abstract Syntax Tree (AST) hierarchy.
  - Implemented Schema Catalog as the compiler's Symbol Table.
  - Built Semantic Analyzer with static type checking and error recovery.
  - Implemented Query Planner generating Relational Algebra Intermediate Representation (IR).
  - Built In-Memory Execution Engine evaluating queries over test relations.
  - Developed full automated test harness and multi-case live demo runner.

---

### SLIDE 3: Review 2 Rubric Alignment (25 Marks)
| Rubric Criterion | Marks | Review 2 Deliverable / Implementation Evidence |
|---|:---:|---|
| **Implementation Progress** | **7** | Full functional pipeline implemented: Lexer $\rightarrow$ Parser $\rightarrow$ AST $\rightarrow$ Semantic $\rightarrow$ Planner $\rightarrow$ Execution. No simulated stages. |
| **Technical Correctness** | **5** | Deterministic predictive parsing, accurate AST synthesis, exact type inference, relational algebraic operator execution. |
| **Compiler Concept Application** | **4** | Applied Lexical Scanning, CFG, LL(1) Recursive Descent, AST nodes, Symbol Table lookup, Static Type Checking, Intermediate Code (IR), and Runtime Interpreter. |
| **Code Quality** | **3** | Clean modular architecture across 8 sub-packages, comprehensive docstrings, meaningful naming, zero external dependencies. |
| **Testing** | **3** | 16-test formal verification matrix + 20 PyUnit test cases covering positive, compound, error, and boundary conditions (100% pass rate). |
| **Individual Understanding** | **3** | Deep architectural command, ability to trace grammar productions, type checking rules, and execution operators during viva. |
| **TOTAL** | **25 / 25** | **Working Prototype & Demonstration Ready** |

---

### SLIDE 4: Core Implementation Architecture
```text
Source Query ("SELECT ... FROM ... WHERE ... ;")
       │
       ▼
1. Lexical Analyzer (Deterministic scanning, position tracking)
       │ (Token Stream)
       ▼
2. Syntax Analyzer / Parser (Recursive-descent LL(1) parsing)
       │ (Abstract Syntax Tree)
       ▼
3. Semantic Analyzer ◄──► Schema Catalog / Symbol Table
   (Scope checking & static type validation)
       │ (Validated & Decorated AST)
       ▼
4. Query Planner / IR Generator
   (Relational algebra: SCAN, FILTER, PROJECT, SORT, LIMIT)
       │ (Logical Query Plan - Intermediate Code)
       ▼
5. In-Memory Execution Engine
   (Predicate evaluation over in-memory relational records)
       │
       ▼
   Formatted ASCII Result Table / Precise Diagnostic Errors
```

---

### SLIDE 5: Compiler Design Concepts Applied in Phase 2
| Compiler Concept | Implementation in QueryLang | Practical Evidence |
|---|---|---|
| **Lexical Analysis** | Regex-based deterministic scanner | Token stream with line and column numbers. |
| **Syntax Analysis** | Hand-written Recursive-Descent Parser | Parses queries according to LL(1) CFG productions. |
| **Abstract Syntax Tree** | OOP node hierarchy (`SelectQueryNode`, `BinaryOpNode`, etc.) | Visual ASCII tree representation of query hierarchy. |
| **Symbol Table Management** | `SchemaCatalog`, `TableSymbol`, `ColumnSymbol` | Multi-table catalog with column data types. |
| **Semantic Analysis** | Table/column scope binding + `TypeChecker` | Detects undeclared attributes and illegal type comparisons. |
| **Intermediate Representation (IR)** | Relational algebra query plan DAG | Decoupled logical plan (`SCAN`, `FILTER`, `PROJECT`). |
| **Execution Engine** | Runtime interpreter and row evaluator | Evaluates operations against in-memory records. |
| **Contextual Error Reporting** | Multi-level exceptions (`Lexical`, `Syntax`, `Semantic`) | Visual caret (`^`) pointing to error token location. |

---

### SLIDE 6: Parser Implementation & Formal Grammar
- **Grammar (EBNF):**
  - `query ::= SELECT column_list FROM table_name [where_clause] [order_clause] [limit_clause] ";"`
  - `column_list ::= "*" | column_name ("," column_name)*`
  - `where_clause ::= WHERE condition`
  - `condition ::= or_expr`
  - `or_expr ::= and_expr ("OR" and_expr)*`
  - `and_expr ::= comparison ("AND" comparison)*`
  - `comparison ::= primary_expr [comp_op primary_expr]`
- **Recursive-Descent Design:**
  - Stratified non-terminals ensure unambiguous operator precedence (`OR` < `AND` < `COMPARE` < `PRIMARY`).
  - Predictive lookahead (`current_token` and `peek()`) ensures linear $O(N)$ execution time.

---

### SLIDE 7: Abstract Syntax Tree (AST) Visualization
For the query:  
`SELECT name, cgpa FROM students WHERE cgpa >= 8.5 AND age > 20;`

```text
SelectQueryNode
|-- Projected Columns: [name, cgpa]
|-- Source Table: students
|-- WHERE Condition:
    \-- BinaryOpNode(AND)
        |-- BinaryOpNode(>=)
        |   |-- ColumnNode(cgpa)
        |   \-- LiteralNode(8.5 : FLOAT)
        \-- BinaryOpNode(>)
            |-- ColumnNode(age)
            \-- LiteralNode(20 : INTEGER)
```

---

### SLIDE 8: Symbol Table (Schema Catalog)
- Implemented in `querylang/schema/catalog.py`.
- Maps table identifiers to column attributes and data types:
  - **`students` Relation:**
    - `id` $\rightarrow$ `INTEGER`
    - `name` $\rightarrow$ `STRING`
    - `age` $\rightarrow$ `INTEGER`
    - `branch` $\rightarrow$ `STRING`
    - `cgpa` $\rightarrow$ `FLOAT`
  - **`departments` Relation:**
    - `dept_id` $\rightarrow$ `INTEGER`, `dept_name` $\rightarrow$ `STRING`, `hod` $\rightarrow$ `STRING`, `building` $\rightarrow$ `STRING`
- Provides fast $O(1)$ scope resolution and attribute validation.

---

### SLIDE 9: Semantic Analysis & Static Type Checking
- **Scope Verification:**
  - Validates table presence in the catalog.
  - Validates projected and condition columns exist within the target table.
- **Type Checking Rules:**
  - Numeric comparisons allowed across `INTEGER` and `FLOAT`.
  - String comparisons allowed between `STRING` and `STRING`.
  - Illegal comparisons flagged: `STRING > INTEGER` $\rightarrow$ `SemanticError`.
- **Informative Diagnostics:**
  - Suggests available columns if an attribute name is misspelled:  
    `HINT: Available columns in 'students': id, name, age, branch, cgpa`

---

### SLIDE 10: Intermediate Representation (Logical Query Plan)
- Translates validated AST into relational algebra operators:
  $$\pi_{\text{name, cgpa}}\left(\sigma_{\text{cgpa} \ge 8.5\ \land\ \text{age} > 20}\left(\text{SCAN}(\text{students})\right)\right)$$
- **Plan Tree Structure:**
```text
\-- PROJECT [name, cgpa]
    \-- FILTER [cgpa >= 8.5 AND age > 20]
        \-- SCAN [students]
```
- Decouples syntax parsing from runtime execution, preparing the architecture for algebraic query rewrites in Phase 3.

---

### SLIDE 11: In-Memory Execution Engine
- Evaluates the logical plan tree against stored in-memory relation tuples.
- Supports projection, relational filtering, sorting (`ORDER BY`), and cardinality limits (`LIMIT`).
- Output format: dynamically formatted ASCII tables with summary metrics:
```text
+--------+--------+
| NAME   | CGPA   |
+--------+--------+
| Asha   | 8.7    |
| Rahul  | 9.1    |
| Pooja  | 8.9    |
| Ananya | 9.4    |
+--------+--------+
4 row(s) in set (Scanned: 7, Filtered: 4)
```

---

### SLIDE 12: Comprehensive Testing Matrix
- **Automated Verification Harness:** `tests/run_all_tests.py`
- **16-Test Verification Matrix:**
  - Positive Projections: `T-01` (Single col), `T-02` (Multi col), `T-06` (Wildcard `*`) $\rightarrow$ **PASS**
  - Filtering & Logic: `T-03` (WHERE), `T-04` (AND), `T-05` (OR) $\rightarrow$ **PASS**
  - Modifiers: `T-07` (ORDER BY), `T-08` (LIMIT) $\rightarrow$ **PASS**
  - Lexical Diagnostics: `T-09` (Illegal char `@`) $\rightarrow$ **PASS**
  - Syntactic Diagnostics: `T-10` (Missing col), `T-11` (Missing FROM) $\rightarrow$ **PASS**
  - Semantic Diagnostics: `T-12` (Unknown table), `T-13` (Unknown col), `T-14` (Type mismatch) $\rightarrow$ **PASS**
  - Boundary Conditions: `T-15` (Empty result set), `T-16` (Stage pipeline check) $\rightarrow$ **PASS**
- **PyUnit Suite:** 20/20 unit tests passed in 0.004s.

---

### SLIDE 13: Live Demonstration Scenarios
1. **Demo 1:** Basic Projection $\rightarrow$ `SELECT name FROM students;`
2. **Demo 2:** Relational Filter $\rightarrow$ `SELECT name, age, cgpa FROM students WHERE age > 20;`
3. **Demo 3:** Semantic Diagnostics $\rightarrow$ Catches missing columns (`SELECT salary...`) & type mismatches (`WHERE name > 50`).
4. **Demo 4:** Syntactic Diagnostics $\rightarrow$ Catches missing columns (`SELECT FROM...`) & missing keywords (`SELECT name students;`).
5. **Demo 5:** Full Pipeline Inspection $\rightarrow$ Traces Token Stream $\rightarrow$ AST $\rightarrow$ Symbol Table $\rightarrow$ Relational Plan $\rightarrow$ Result Table.

---

### SLIDE 14: Conclusion & Phase 3 Roadmap
- **Review 2 Milestones Accomplished:**
  - Transitioned from a lexer prototype to a complete, functioning language processing system.
  - Successfully demonstrated all core compiler concepts from tokenization to execution.
- **Phase 3 Planned Enhancements:**
  - **Query Optimizer:** Rule-based algebraic optimizations (predicate pushdown, constant folding, tautology elimination).
  - **Language Extensions:** Multi-table JOIN operations and aggregate functions (`COUNT`, `AVG`, `SUM`).
  - **Performance Benchmarking:** Comparative timing between original vs. optimized plans over 100 to 10,000 records.
  - **Visual Interface:** GUI / web-based visual pipeline inspector.
