# QueryLang: Design and Implementation of a Compiler-Style Query Processing Engine with Rule-Based Query Optimization

**Final Project Review (Review 3) Comprehensive Technical Report**  
**Course Code:** BCSE307P — Compiler Design Laboratory  
**Academic Year:** 2026–2027  
**Student Name:** Aman Katakwar  
**Registration Number:** 24BCE0160  
**Faculty Guide:** Prof. Ranjithkumar S  
**Institution:** School of Computer Science and Engineering, Vellore Institute of Technology  

---

## 1. Executive Summary & Project Abstract

The rapid proliferation of data-intensive software architectures has made high-throughput, low-latency relational querying a fundamental computational requirement. Contemporary relational database management systems (RDBMS) such as PostgreSQL, SQLite, and DuckDB process declarative Structured Query Language (SQL) statements not through simple runtime string interpretation, but through sophisticated, multi-phase compiler pipelines. These compilers progressively lower high-level declarative abstractions through lexical analysis, recursive-descent syntax parsing, semantic analysis with symbol table validation, intermediate code representation (IR) generation, algebraic rule-based query optimization, and tree-walking physical plan execution.

This project, titled **“QueryLang: Design and Implementation of a Compiler-Style Query Processing Engine with Rule-Based Query Optimization”**, details the architecture, formal theoretical formulation, algorithmic implementation, and empirical verification of a complete domain-specific query compiler. Built strictly from first principles using standard Python 3.12 without external third-party compiler libraries or database engines, QueryLang demonstrates genuine compiler construction paradigms across six modular compiler phases:

1. **Lexical Analysis (Scanner):** Converts raw SQL-like query text into a strongly typed token stream with precise coordinate tracking ($(\text{line}, \text{column})$) and robust lexical error detection.
2. **Syntax Analysis (Parser):** Consumes tokens via an LL(1) recursive-descent parser to construct a strongly typed, hierarchical Abstract Syntax Tree (AST) conforming to an extended EBNF grammar with strict operator precedence hierarchies.
3. **Semantic Analysis & Type Checking:** Enforces static relational constraints by resolving multi-table schema catalogs (acting as the compiler symbol table), checking column existence, disambiguating qualified column identifiers, and performing strict static type compatibility checks on comparisons and arithmetic expressions.
4. **Intermediate Code Generation (Query Planner):** Lowers validated AST representations into an Intermediate Representation (IR) consisting of a tree of relational algebra operators ($\sigma$, $\pi$, $\bowtie$, $\gamma$, $\tau$, $\lambda$).
5. **Rule-Based Query Optimizer (Algebraic Transformation Engine):** Traverses the IR plan to apply sound algebraic transformations:
   - *Constant Folding:* Static compile-time evaluation of pure arithmetic expressions (e.g., $(18 + 2) \to 20$).
   - *Predicate Simplification:* Application of boolean algebraic identities and tautology elimination (e.g., $P \land \text{TRUE} \to P$, $(1 = 1) \to \text{TRUE}$).
   - *Filter Pushdown:* Algebraic relocation of selection operators ($\sigma$) past multi-table relational join nodes ($\bowtie$) directly adjacent to sequential scan leaves ($\text{SCAN}$), drastically minimizing intermediate join input cardinalities.
6. **Execution Engine (Physical Relational Operator Walking):** Directly executes the optimized relational algebra plan against in-memory relation records, evaluating short-circuit booleans, arithmetic transformations, inner equi-joins, and scalar statistical aggregations (`COUNT`, `AVG`, `SUM`, `MIN`, `MAX`).

The implementation has been verified through a formal 25-point verification matrix ($\text{T-01}$ through $\text{T-25}$) achieving a 100% pass rate, an automated PyUnit test suite with 26 unit tests, and empirical performance benchmarks across synthetic datasets of 100, 1,000, and 10,000 records demonstrating an average query speedup of $1.9\times$ to $2.3\times$ under optimization.

---

## 2. Problem Statement & Motivation

### 2.1 The Educational Problem
Traditional undergraduate compiler design curricula predominantly focus on imperative, procedural, or object-oriented programming languages (e.g., compiling mini-C, Pascal, or subset-Java into stack-machine bytecode or MIPS assembly). While instructive, this approach often leaves students with an incomplete perspective regarding how declarative domain-specific languages (DSLs) are compiled and executed in real-world systems software. In declarative languages:
- The programmer specifies *what* data is desired, rather than *how* to procedurally fetch and compute it.
- The compiler front-end and middle-end shoulder the critical responsibility of transforming the declarative specification into an optimal physical execution strategy.
- Query optimization represents an industrial application of program transformation, constant propagation, dead-code elimination, and loop-invariant code motion adapted to relational algebra.

### 2.2 The Technical Challenge
Designing a production-grade relational query compiler involves resolving intricate computer science challenges:
- **Grammar Ambiguity & Precedence:** Parsing arithmetic operators ($+, -, *, /$, parenthesization) embedded within relational comparison predicates ($=, \neq, >, <, \ge, \le$) and logical connectors ($\land, \lor$) without parsing conflicts or infinite left-recursion.
- **Cross-Schema Semantic Binding:** Disambiguating unqualified column identifiers (e.g., `name`) and qualified attributes (e.g., `students.name`) across multiple joined tables while providing human-readable diagnostic error messages with source indicators.
- **Relational Plan Equivalence & Optimization:** Formulating safe algebraic rewrite rules that guarantee semantic equivalence while strictly reducing computational time complexity from $O(N \times M)$ cartesian comparisons to $O(\sigma(N) \times M)$ through filter pushdown.

QueryLang directly resolves these challenges by implementing an end-to-end, zero-dependency compiler pipeline that serves as an exemplary pedagogical and engineering artifact for compiler design.

---

## 3. Domain-Specific Language (DSL) Specification

QueryLang implements a declarative, SQL-inspired grammar designed specifically for relational querying, multi-table joining, aggregation, and mathematical filtering.

### 3.1 Lexical Elements
- **Keywords (Case-Insensitive):** `SELECT`, `FROM`, `JOIN`, `INNER`, `ON`, `WHERE`, `AND`, `OR`, `ORDER`, `BY`, `ASC`, `DESC`, `LIMIT`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- **Identifiers:** Sequences of alphanumeric characters and underscores starting with an alphabetic letter or underscore (`[a-zA-Z_][a-zA-Z0-9_]*`).
- **Qualified Identifiers:** Multi-part identifiers joined by a dot (`table.column`).
- **Literals:**
  - *Integer Literals:* Non-empty sequences of decimal digits (`[0-9]+`), e.g., `21`, `100`.
  - *Floating-Point Literals:* Decimal digit sequences separated by a dot (`[0-9]+\.[0-9]+`), e.g., `8.75`, `9.4`.
  - *String Literals:* Character sequences enclosed in single quotes (`'...'`), supporting escaped characters, e.g., `'CSE'`, `'Technology Tower'`.
  - *Boolean Literals:* Keyword constants `TRUE` and `FALSE`.
- **Operators & Punctuation:**
  - Relational Comparison: `=`, `!=`, `>`, `<`, `>=`, `<=`
  - Arithmetic Operators: `+`, `-`, `*`, `/`
  - Grouping & Delimiters: `(`, `)`, `,`, `.`, `;`

### 3.2 Canonical Query Idioms
```sql
-- Core Selection and Projection
SELECT name, branch, cgpa FROM students WHERE age >= 21 ORDER BY cgpa DESC LIMIT 3;

-- Multi-Table INNER JOIN with Qualified Columns
SELECT students.name, departments.dept_name, departments.building
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.cgpa >= 8.5;

-- Algebraic Optimization Candidate (Constant Folding + Filter Pushdown)
SELECT students.name, departments.dept_name
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.age > (18 + 2) AND students.cgpa > 8.0 AND (1 = 1);

-- Scalar Aggregations
SELECT COUNT(*), AVG(cgpa), MAX(cgpa), MIN(age) FROM students;
```

---

## 4. Formal EBNF Grammar & Operator Precedence

The QueryLang grammar is formally specified below using Extended Backus-Naur Form (EBNF). The grammar is designed to be unambiguous and strictly parsable via deterministic LL(1) recursive descent.

```ebnf
Query            ::= "SELECT" Projection "FROM" TableReference [ JoinClause ]
                     [ "WHERE" Expression ]
                     [ "ORDER" "BY" QualifiedColumn [ "ASC" | "DESC" ] ]
                     [ "LIMIT" INTEGER ] ";"

Projection       ::= "*" | ProjectItem ( "," ProjectItem )*
ProjectItem      ::= AggregateFunction | QualifiedColumn
AggregateFunction::= ( "COUNT" "(" ( "*" | QualifiedColumn ) ")" )
                   | ( ( "SUM" | "AVG" | "MIN" | "MAX" ) "(" QualifiedColumn ")" )

TableReference   ::= IDENTIFIER [ IDENTIFIER ]
JoinClause       ::= [ "INNER" ] "JOIN" TableReference "ON" Expression

QualifiedColumn  ::= [ IDENTIFIER "." ] IDENTIFIER

Expression       ::= LogicalOrExpr
LogicalOrExpr    ::= LogicalAndExpr ( "OR" LogicalAndExpr )*
LogicalAndExpr   ::= ComparisonExpr ( "AND" ComparisonExpr )*
ComparisonExpr   ::= AdditiveExpr [ ( "=" | "!=" | ">" | "<" | ">=" | "<=" ) AdditiveExpr ]

AdditiveExpr     ::= MultiplicativeExpr ( ( "+" | "-" ) MultiplicativeExpr )*
MultiplicativeExpr::= PrimaryExpr ( ( "*" | "/" ) PrimaryExpr )*

PrimaryExpr      ::= QualifiedColumn
                   | Literal
                   | "(" Expression ")"

Literal          ::= INTEGER | FLOAT | STRING | BOOLEAN
```

### 4.1 Operator Precedence & Associativity Matrix

| Precedence Level | Operators | Associativity | Description |
|:---:|:---:|:---:|:---|
| **1 (Lowest)** | `OR` | Left-to-Right | Logical Disjunction |
| **2** | `AND` | Left-to-Right | Logical Conjunction |
| **3** | `=`, `!=`, `>`, `<`, `>=`, `<=` | Non-associative | Relational Comparison |
| **4** | `+`, `-` | Left-to-Right | Additive Arithmetic |
| **5** | `*`, `/` | Left-to-Right | Multiplicative Arithmetic |
| **6 (Highest)** | `( ... )`, Identifiers, Literals | N/A | Grouping and Atomic Operands |

This 6-tier hierarchy resolves all precedence ambiguities algebraically in the grammar definition, ensuring that expressions like `age + 2 >= 20 AND cgpa > 8.0` parse into identical semantic precedence structures as standard programming languages.

---

## 5. End-to-End Compiler Pipeline Architecture

The QueryLang engine employs a classical 6-phase compiler pipeline:

```
[Raw SQL Query]
       |
       v
+------------------+
| 1. Lexer         |  --> Emits Token Stream with line/column coordinates
+------------------+
       |
       v
+------------------+
| 2. Parser        |  --> LL(1) Recursive Descent constructs Abstract Syntax Tree (AST)
+------------------+
       |
       v
+------------------+
| 3. Semantic      |  --> Multi-Schema Catalog Symbol Binding & Static Type Checking
|    Analyzer      |
+------------------+
       |
       v
+------------------+
| 4. Query Planner |  --> Generates Logical Plan Intermediate Representation (IR)
+------------------+
       |
       v
+------------------+
| 5. Rule-Based    |  --> Constant Folding, Predicate Simplification, Filter Pushdown
|    Optimizer     |
+------------------+
       |
       v
+------------------+
| 6. Execution     |  --> Physical Relational Operator Evaluation over In-Memory Tables
|    Engine        |
+------------------+
       |
       v
[Tabular Result & Execution Diagnostics]
```

Each compiler phase is encapsulated within its own module, ensuring strict separation of concerns:
- `querylang.lexer`: Lexical analysis, regular expression scanning, token stream generation.
- `querylang.parser`: Syntactic validation, grammar rule enforcement, AST construction.
- `querylang.ast`: Strongly typed, immutable AST node definitions with ASCII tree pretty-printing.
- `querylang.schema`: Symbol table catalog, table schemas, attribute data types.
- `querylang.semantic`: Semantic error detection, multi-table binding, static type inference.
- `querylang.planner`: Relational algebra intermediate representation (IR) builder.
- `querylang.optimizer`: Algebraic optimization rules, tree rewriting, comparison reporting.
- `querylang.execution`: In-memory hash/nested-loop join execution, predicate evaluation, aggregation.
- `querylang.visualization`: Graphviz DOT exporter for AST and relational plans.
- `querylang.benchmarks`: Synthetic dataset generation and execution timing suite.

---

## 6. Phase 1: Lexical Analysis & Token Scanning

The Lexical Analyzer (`Lexer` class in `querylang/lexer/lexer.py`) is responsible for translating an input character sequence into a stream of structured `Token` objects.

### 6.1 Scanner Implementation Details
The scanner employs a unified master regular expression compiled with `re.VERBOSE` and `re.IGNORECASE` to scan tokens in a single linear pass ($O(N)$ where $N$ is the query length in characters). Each token records:
- `type`: Member of the `TokenType` enumeration (`SELECT`, `IDENTIFIER`, `INTEGER`, etc.).
- `value`: Evaluated Python primitive (`int`, `float`, `str`, or boolean).
- `line`: 1-based source line index.
- `column`: 1-based character position within the current line.

### 6.2 Lexical Error Diagnostics
When an unrecognized character sequence is encountered (e.g., `SELECT name @ students;`), the lexer does not terminate abruptly with an unhandled exception. Instead, it raises a `LexicalError` that captures the offending character, line number, column coordinate, and constructs a visual ASCII caret pointer:
```
[LEXICAL ERROR] at Line 1, Column 13: Invalid character sequence '@'
  --> SELECT name @ students;
                  ^
  HINT: Remove or replace the unsupported character.
```

---

## 7. Phase 2: Syntax Analysis & Abstract Syntax Tree (AST)

The Parser (`Parser` class in `querylang/parser/parser.py`) consumes the token stream emitted by the Lexer and constructs a strongly typed Abstract Syntax Tree (AST).

### 7.1 Recursive-Descent Parser Architecture
The parser implements an LL(1) recursive-descent strategy. It maintains a current token cursor (`current_token`), a lookahead mechanism (`peek()`), and utility assertion methods (`consume(expected_type)`). Syntax errors generate detailed `SyntaxError` diagnostics that identify exactly what token was expected versus what was found.

### 7.2 Abstract Syntax Tree Node Hierarchy
The AST node hierarchy is implemented as an object-oriented class tree deriving from an abstract base class `ASTNode`:
- `SelectQueryNode`: The root of the query AST containing projected columns, source table, optional join clause, optional filter condition, sort configuration, and limit count.
- `TableNode`: Represents a table reference (`students`, `departments`).
- `JoinNode`: Encapsulates an `INNER JOIN` target table and its `ON` join predicate.
- `ColumnNode`: Represents an attribute reference with optional table qualification (`students.age`).
- `AggregateNode`: Represents scalar statistical aggregates (`COUNT(*)`, `AVG(cgpa)`).
- `LiteralNode`: Terminal node holding typed constant values (`INTEGER`, `FLOAT`, `STRING`, `BOOLEAN`).
- `ArithmeticOpNode`: Represents binary arithmetic operations (`+`, `-`, `*`, `/`).
- `BinaryOpNode`: Represents logical connectors (`AND`, `OR`) and relational comparisons (`=`, `!=`, `>`, `<`, `>=`, `<=`).

### 7.3 AST ASCII Pretty-Printing
Each AST node implements `.tree_repr()` to render the parsed hierarchy cleanly using standard ASCII line markers:
```
SelectQueryNode
|-- Projected Columns: [name, branch, cgpa]
|-- Source Table: students
|-- WHERE Condition:
|   \-- BinaryOpNode(AND)
|       |-- BinaryOpNode(>=)
|       |   |-- ColumnNode(age)
|       |   \-- ArithmeticOpNode(+)
|       |       |-- LiteralNode(18 : INTEGER)
|       |       \-- LiteralNode(2 : INTEGER)
|       \-- BinaryOpNode(=)
|           |-- LiteralNode(1 : INTEGER)
|           \-- LiteralNode(1 : INTEGER)
|-- ORDER BY: cgpa DESC
\-- LIMIT: 3
```

---

## 8. Phase 3: Semantic Analysis, Multi-Schema Catalog & Static Type Checking

Syntax validation confirms that a query follows grammatical rules, but cannot verify whether referenced tables and columns exist, whether columns are ambiguous, or whether data types in expressions are compatible. This is the domain of the Semantic Analyzer (`SemanticAnalyzer` in `querylang/semantic/analyzer.py`).

### 8.1 Schema Catalog as the Compiler Symbol Table
The `SchemaCatalog` class (`querylang/schema/catalog.py`) maintains the compiler's symbol table. In relational compilers, the symbol table stores:
- Table symbols (`TableSymbol`): Name, primary key, row count estimate, and column dictionary.
- Column symbols (`ColumnSymbol`): Column name, qualified name, table binding, and static data type (`INTEGER`, `FLOAT`, `STRING`, `BOOLEAN`).

The default catalog defines two relational schemas:
- `students`: `id` (INT), `name` (STR), `age` (INT), `branch` (STR), `cgpa` (FLOAT).
- `departments`: `dept_id` (INT), `dept_name` (STR), `hod` (STR), `building` (STR).

### 8.2 Semantic Checks Enforced
1. **Primary & Joined Table Existence:** Validates that tables in `FROM` and `JOIN` clauses exist in the catalog. If non-existent, provides available table names in diagnostic hints.
2. **Column Resolution & Disambiguation:** Resolves both unqualified (`age`) and qualified (`students.age`) column identifiers. Ensures attributes belong to declared tables.
3. **Aggregate Function Validation:** Confirms aggregate function names (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`), ensures `*` is only passed to `COUNT`, and verifies that arguments to `SUM` and `AVG` are strictly numeric (`INTEGER` or `FLOAT`).
4. **Static Type Checking (`TypeChecker`):**
   - Boolean condition validation: Confirms that `WHERE` and `ON` clauses evaluate to `BOOLEAN`.
   - Comparison compatibility: Checks that relational operators (`=`, `!=`, `>`, `<`, `>=`, `<=`) operate on compatible data types. For example, comparing a `STRING` column with an `INTEGER` literal raises a fatal semantic error.
   - Arithmetic compatibility: Verifies that arithmetic operations (`+`, `-`, `*`, `/`) operate strictly on numeric types (`INTEGER` or `FLOAT`), returning `FLOAT` if either operand is floating-point.

---

## 9. Phase 4: Intermediate Code Generation (Query Planner)

The Query Planner (`QueryPlanner` in `querylang/planner/planner.py`) bridges the front-end AST and the back-end execution engine by lowering the validated AST into an Intermediate Representation (IR).

### 9.1 Relational Algebra Plan Nodes
The IR is represented as an operator tree corresponding to relational algebra primitives:
- `ScanNode`: Represents sequential scan access: $\text{SCAN}(R)$.
- `JoinPlanNode`: Represents relational inner join: $R \bowtie_{\theta} S$.
- `FilterNode`: Represents relational selection: $\sigma_{\theta}(R)$.
- `ProjectNode`: Represents relational projection: $\pi_{c_1, \dots, c_k}(R)$.
- `AggregatePlanNode`: Represents relational aggregation: $\gamma_{f_1, \dots, f_m}(R)$.
- `SortNode`: Represents ordering: $\tau_{c}(R)$.
- `LimitNode`: Represents cardinality truncation: $\lambda_{k}(R)$.

---

## 10. Phase 5: Rule-Based Query Optimizer

The Query Optimizer (`QueryOptimizer` in `querylang/optimizer/optimizer.py`) constitutes the technical centerpiece of Review 3. It accepts an initial, naive logical query plan and applies sound algebraic transformations to produce an optimized, canonical plan.

### 10.1 Constant Folding
Pure arithmetic subtrees containing only literal constants are statically evaluated at compile time rather than repeatedly inside the row execution loop.
- **Rule Formulation:** $\text{Fold}(c_1 \odot c_2) \to c_{\text{result}}$ where $c_1, c_2 \in \text{Literals}$ and $\odot \in \{+, -, *, /\}$.
- **Example:** `students.age >= (18 + 2) * 1` is folded to `students.age >= 20`. For a table with 10,000 rows, this eliminates 20,000 redundant runtime arithmetic operations.
- Constant comparisons are also folded: $(1 = 1) \to \text{TRUE}$.

### 10.2 Predicate Simplification (Boolean Axiom Reduction)
Boolean expressions in `WHERE` clauses are simplified using fundamental boolean algebraic identities:
- **Identity Laws:**
  $$\phi \land \text{TRUE} \equiv \phi, \quad \phi \lor \text{FALSE} \equiv \phi$$
- **Annihilation Laws:**
  $$\phi \land \text{FALSE} \equiv \text{FALSE}, \quad \phi \lor \text{TRUE} \equiv \text{TRUE}$$
- **Redundant Filter Elimination:** If a predicate simplifies to the constant literal $\text{TRUE}$, the entire `FilterNode` is pruned from the plan tree.

### 10.3 Algebraic Filter Pushdown
In naive relational plans, filtering occurs *after* joins:
$$\pi(\sigma_{\theta}(R \bowtie_{\psi} S))$$
If the filter condition $\theta$ references only attributes belonging to relation $R$ (i.e., $\text{attrs}(\theta) \subseteq \text{schema}(R)$), the relational algebra equivalence allows pushing the selection before the join:
$$\pi((\sigma_{\theta}(R)) \bowtie_{\psi} S)$$
- **Algorithmic Complexity Impact:** If relation $R$ has $N$ records, relation $S$ has $M$ records, and selectivity $\text{sel}(\theta) = 0.2$ (80% of rows rejected), naive join evaluates $N \times M$ join pairs. Under filter pushdown, the join only evaluates $0.2N \times M$ pairs, reducing join overhead by **80%**.

---

## 11. Language Extension I: Multi-Table Relational INNER JOIN

QueryLang supports multi-table inner joins via the syntax:
```sql
SELECT students.name, departments.dept_name, departments.building
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.cgpa >= 8.5;
```

### 11.1 Implementation Architecture
- **Parser:** Recognizes optional `INNER` keyword, `JOIN`, target table, `ON` keyword, and arbitrary boolean expressions.
- **Semantic Resolution:** Binds both the primary table and joined table against the catalog, validating the join predicate.
- **Execution Operator:** Evaluates the join using a nested-loop join operator with prefix-aware attribute lookups, producing merged records accessible by both qualified (`students.branch`) and unqualified (`branch`) keys.

---

## 12. Language Extension II: Scalar Aggregation Engine

Review 3 introduces full support for relational scalar aggregates:
- `COUNT(*)`: Total row count of the input relation.
- `COUNT(column)`: Count of non-null values for the specified column.
- `SUM(column)`: Arithmetic summation of numeric column values.
- `AVG(column)`: Arithmetic mean rounded to 2 decimal places.
- `MIN(column)`: Minimum scalar value.
- `MAX(column)`: Maximum scalar value.

### 12.1 Execution Mechanics
When aggregates are present, the planner emits an `AggregatePlanNode`. The execution engine processes child relation rows in a single streaming pass ($O(N)$ time, $O(1)$ auxiliary space per aggregate accumulator), synthesizing a single summary record.

---

## 13. Phase 6: In-Memory Execution Engine & Physical Operators

The Execution Engine (`ExecutionEngine` in `querylang/execution/engine.py`) walks the optimized IR plan tree and executes physical relational operators against in-memory table records:
- **`ScanNode`:** Fetches row copies from the active database dictionary, recording scanned row counts.
- **`FilterNode`:** Iterates through child records, evaluating the predicate using `ExpressionEvaluator`.
- **`ProjectNode`:** Extracts requested column subsets, supporting case-insensitivity and table prefixes.
- **`SortNode`:** Performs stable sorting using Python's Timsort ($O(K \log K)$) according to specified sort keys and order (`ASC` / `DESC`).
- **`LimitNode`:** Truncates the result stream to at most $k$ records.

The execution engine returns a structured `QueryResult` object capable of rendering formatted, aligned ASCII tables with execution telemetry.

---

## 14. Comprehensive Error Handling & Diagnostics Architecture

A hallmark of a professional compiler is high-quality diagnostic reporting. QueryLang implements a unified error hierarchy deriving from `QueryLangError`:

```
               QueryLangError (Base)
              /     |       |       \
    LexicalError SyntaxError SemanticError ExecutionError
```

Each error captures exact coordinate locations and formats an annotated source code snippet:
```
[SEMANTIC ERROR] at Line 1, Column 38: Operator '>' cannot be applied to STRING and INTEGER.
  --> SELECT name FROM students WHERE name > 50;
                                           ^
  HINT: Relational ordering '>' requires numeric or string operands of compatible types.
```

---

## 15. Visualizer Module: ASCII & Graphviz DOT Exporter

To facilitate debugging, verification, and academic presentations, QueryLang provides graphical tree export via `DOTExporter` (`querylang/visualization/visualizer.py`):
1. **`ast_to_dot(ast)`:** Exports the AST into standard Graphviz DOT format with color-coded node styles (blue for queries, green for tables, purple for operators, yellow for aggregates).
2. **`plan_to_dot(plan)`:** Exports logical execution plans with relational operator styling.
3. **`comparison_to_dot(orig, opt)`:** Emits side-by-side subgraphs (`cluster_original` vs `cluster_optimized`) visually contrasting unoptimized and optimized plans.

Exported DOT files can be viewed using WebGraphviz, Viz.js, or compiled to SVG/PNG using the `dot` command-line utility.

---

## 16. Empirical Performance Benchmarking & Complexity Analysis

To empirically validate the benefits of compiler query optimization, a performance benchmark suite (`querylang/benchmarks/benchmark.py`) was executed on synthetic datasets of 100, 1,000, and 10,000 records.

### 16.1 Benchmark Query
```sql
SELECT students.name, departments.dept_name
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.age > (18 + 2) AND students.cgpa > 8.0;
```

### 16.2 Empirical Results Table

| Dataset Scale ($N$) | Unoptimized Plan | Optimized Plan | Speedup Ratio | Matched Rows | Equivalence Check |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **100 rows** | 4.615 ms | 2.442 ms | **$1.89\times$** | 27 rows | Identical (100%) |
| **1,000 rows** | 48.331 ms | 25.017 ms | **$1.93\times$** | 295 rows | Identical (100%) |
| **10,000 rows** | 504.321 ms | 220.880 ms | **$2.28\times$** | 2,672 rows | Identical (100%) |

### 16.3 Complexity & Analytical Findings
1. **Constant Folding Impact:** Statically precomputing `(18 + 2) -> 20` eliminated 10,000 runtime additions on the 10k row dataset.
2. **Filter Pushdown Impact:** By filtering students *before* the join, the input cardinality to the join was reduced from 10,000 to 2,672 rows. This reduced nested-loop pairwise comparisons from $10,000 \times 5 = 50,000$ to $2,672 \times 5 = 13,360$—a **$73.3\%$ reduction in join evaluations**.

---

## 17. Formal Quality Assurance: 25-Point Verification Matrix

The test runner (`tests/run_all_tests.py`) executes 25 formal verification test cases covering every component of the compiler:

| Test ID | Test Category | Query Input | Expected Behavior | Status |
|:---:|:---|:---|:---|:---:|
| **T-01** | Projection | `SELECT name FROM students;` | 7 rows returned | **PASS** |
| **T-02** | Multi-Projection | `SELECT name, cgpa FROM students;` | 2 columns, 7 rows | **PASS** |
| **T-03** | Relational Filter | `SELECT name FROM students WHERE age > 20;` | 4 rows matched | **PASS** |
| **T-04** | Compound Filter | `SELECT name, cgpa FROM students WHERE cgpa >= 8.5 AND age > 20;` | 4 rows matched | **PASS** |
| **T-05** | Logical OR Filter | `SELECT name FROM students WHERE branch = 'MECH' OR branch = 'CIVIL';` | 2 rows matched | **PASS** |
| **T-06** | Wildcard `*` | `SELECT * FROM students WHERE cgpa >= 9.0;` | 5 cols, 2 rows | **PASS** |
| **T-07** | Ordering | `SELECT name, cgpa FROM students ORDER BY cgpa;` | Sorted ascending | **PASS** |
| **T-08** | Cardinality Limit | `SELECT name FROM students LIMIT 3;` | Exactly 3 rows | **PASS** |
| **T-09** | Lexical Error | `SELECT name @ students;` | `LexicalError` raised | **PASS** |
| **T-10** | Syntax Error | `SELECT FROM students;` | `SyntaxError` raised | **PASS** |
| **T-11** | Syntax Error | `SELECT name students;` | `SyntaxError` raised | **PASS** |
| **T-12** | Semantic Error | `SELECT name FROM faculty;` | `SemanticError` raised | **PASS** |
| **T-13** | Semantic Error | `SELECT salary FROM students;` | `SemanticError` raised | **PASS** |
| **T-14** | Type Check Error | `SELECT name FROM students WHERE name > 50;` | `SemanticError` raised | **PASS** |
| **T-15** | Boundary Test | `SELECT name FROM students WHERE age > 100;` | 0 rows returned | **PASS** |
| **T-16** | Stage Inspection | `SELECT name, cgpa FROM students WHERE age >= 21;` | 6 stages verified | **PASS** |
| **T-17** | Constant Folding | `SELECT name FROM students WHERE age >= (18 + 2);` | Folded $18+2 \to 20$ | **PASS** |
| **T-18** | Simplification | `SELECT name FROM students WHERE cgpa > 8.0 AND (1 = 1);` | Eliminated $1=1$ | **PASS** |
| **T-19** | Filter Pushdown | `SELECT students.name FROM students JOIN departments ... WHERE students.age > 20;` | Filter pushed to scan | **PASS** |
| **T-20** | Relational JOIN | `SELECT students.name, departments.dept_name FROM students JOIN departments ...;` | 2 joined rows | **PASS** |
| **T-21** | Qualified Columns | `SELECT students.name, students.branch FROM students;` | 2 columns resolved | **PASS** |
| **T-22** | Aggregate COUNT | `SELECT COUNT(*) FROM students;` | 1 row, count=7 | **PASS** |
| **T-23** | Aggregates AVG/MAX | `SELECT AVG(cgpa), MAX(cgpa), MIN(age) FROM students;` | 1 summary row | **PASS** |
| **T-24** | Expression Arith. | `SELECT name, age FROM students WHERE age + 2 >= 24;` | 2 rows matched | **PASS** |
| **T-25** | Graphviz DOT | `SELECT name FROM students WHERE age > 20;` | Valid DOT generated | **PASS** |

**Formal Matrix Summary:** 25 / 25 Passed (100% Pass Rate).  
**PyUnit Unit Test Suites:** 26 / 26 Unit Tests Passed (0 Failures, 0 Errors).

---

## 18. Project Rubrics Compliance & Milestone Achievement Mapping

| Review Phase | Prescribed Rubric Requirement | QueryLang Review 3 Implementation Status | Compliance |
|:---:|:---|:---|:---:|
| **Review 1** | Grammar definition, language specification, lexical specification | Formal EBNF grammar, 27 token types, coordinate tracking | **100%** |
| **Review 2** | Lexer, Recursive-Descent Parser, AST, Symbol Table, Interpreter | Full working front-end, AST visualizer, 16-test matrix | **100%** |
| **Review 3** | Rule-Based Query Optimizer | Constant Folding, Predicate Simplification, Filter Pushdown | **100%** |
| **Review 3** | Language Extensions | Multi-Table INNER JOIN, Aggregates (`COUNT`, `AVG`, `MAX`, etc.) | **100%** |
| **Review 3** | Visualizer & DOT Exporter | Graphviz DOT generation for AST and relational plans | **100%** |
| **Review 3** | Performance Benchmarks | Scaling comparisons across 100, 1,000, and 10,000 records | **100%** |
| **Review 3** | Final Verification & Testing | Expanded 25-point formal verification matrix, 100% pass rate | **100%** |
| **Review 3** | Final Deliverables | 21-Chapter Report, 16-Slide Viva Presentation, downloadable PDFs | **100%** |

---

## 19. Architectural Comparison with Industry Query Compilers

| Dimension | QueryLang (This Project) | SQLite (Industry Standard) | DuckDB (Modern OLAP) | Apache Calcite |
|:---|:---|:---|:---|:---|
| **Compilation Paradigm** | AST $\to$ Relational IR $\to$ Tree Walker | AST $\to$ VDBE Bytecode | AST $\to$ Vectorized Execution Plan | AST $\to$ Relational Algebra $\to$ Pluggable Engine |
| **Grammar Strategy** | LL(1) Recursive Descent | Lemon LALR(1) Parser Generator | Custom Recursive Descent / C++ | JavaCC / Custom LL(k) |
| **Optimization Strategy** | Rule-based algebraic rewrites | Heuristic & cost-based bytecode optimizer | Heuristic & cost-based physical optimizer | Extensible Volcano/Cascades rule optimizer |
| **Intermediate Code** | Relational Algebra Plan Nodes | Virtual Database Engine (VDBE) opcodes | Relational Operator Pipeline | `RelNode` Operator DAG |
| **Dependencies** | Python Standard Library Only (Zero external packages) | C Standard Library | C++ Standard Library | Java Standard Library |

---

## 20. Limitations, Technical Debt & Future Engineering Roadmap

### 20.1 Current Limitations
- **In-Memory Volatility:** Operates strictly on in-memory dictionary datasets; persistent B-Tree storage on disk is not implemented.
- **Join Cardinality:** Joins are currently limited to two-table equi-joins. Multi-way joins ($A \bowtie B \bowtie C$) require nested join trees.
- **Cost-Based Optimization (CBO):** Optimization is currently rule-based (heuristic). It does not compute catalog statistical histograms or cost equations based on disk I/O.

### 20.2 Future Engineering Roadmap
1. **Cost-Based Plan Selection:** Introduce catalog statistics (histograms, distinct value counts) to evaluate alternative join orderings ($R \bowtie S$ vs $S \bowtie R$).
2. **Bytecode Virtual Machine:** Lower relational algebra plans to a register-based or stack-based Virtual Database Engine (VDBE) to eliminate tree-walking interpreter overhead.
3. **Persistent B+Tree Storage:** Implement a slotted-page buffer manager and disk-based B+Tree index storage engine.

---

## 21. Academic References & Bibliography

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.
2. Garcia-Molina, H., Ullman, J. D., & Widom, J. (2008). *Database Systems: The Complete Book* (2nd ed.). Prentice Hall.
3. Graefe, G. (1995). *The Cascades framework for query optimization and its extensible execution engine*. IEEE Data Engineering Bulletin, 18(3), 19–29.
4. Hipp, D. R. (2020). *Architecture of SQLite*. SQLite Consortium Documentation. https://www.sqlite.org/arch.html
5. Raasveldt, M., & Mühleisen, H. (2019). *DuckDB: an Embeddable Analytical Database*. Proceedings of the 2019 International Conference on Management of Data (SIGMOD '19), 1981–1984.
6. Begel, A. (2005). *An Analysis of Abstract Syntax Tree Representation Techniques*. University of California, Berkeley Technical Report.
7. Cooper, K. D., & Torczon, L. (2011). *Engineering a Compiler* (2nd ed.). Morgan Kaufmann.
