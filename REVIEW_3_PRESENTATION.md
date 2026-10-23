# QueryLang: A Compiler-Style Query Processing Engine with Rule-Based Query Optimization

**Review 3 (Final Project Review) Technical Presentation**  
**Course Code:** BCSE307P — Compiler Design Laboratory  
**Academic Year:** 2026–2027  
**Student Name:** Aman Katakwar  
**Registration Number:** 24BCE0160  
**Faculty Guide:** Prof. Ranjithkumar S  
**Institution:** School of Computer Science and Engineering, Vellore Institute of Technology  

---

## Slide 1: Title Slide & Project Overview

### QueryLang: Design and Implementation of a Compiler-Style Query Processing Engine with Rule-Based Query Optimization
*Final Project Review (Review 3) Evaluation & Viva Defense*

- **Candidate:** Aman Katakwar (Registration Number: `24BCE0160`)
- **Faculty Guide:** Prof. Ranjithkumar S
- **Course:** BCSE307P — Compiler Design Laboratory
- **Core Technology Stack:** Python 3.12 (Standard Library Only — Zero External Dependencies)
- **Primary Deliverables:** Complete 6-phase compiler pipeline, rule-based query optimizer, multi-table inner joins, aggregation engine, Graphviz DOT visualizer, performance benchmarks, and formal 25-test verification matrix.

---

## Slide 2: Executive Summary & Project Vision

### Bridging Compiler Theory with High-Performance Relational Systems
- **Industrial Reality:** Modern database engines (SQLite, PostgreSQL, DuckDB, Apache Calcite) are fundamentally **domain-specific compilers** that parse, semantically validate, optimize, and execute declarative query programs.
- **The QueryLang Vision:** Implement an end-to-end, compiler-style query processing engine from first principles to demonstrate classical compiler construction techniques on declarative languages:
  1. Lexical Analysis (Scanner with coordinate tracking).
  2. Syntactic Analysis (LL(1) Recursive-Descent Parser $\to$ AST).
  3. Semantic Analysis (Multi-schema symbol table & static type checking).
  4. Intermediate Representation (Relational algebra logical query plans).
  5. Rule-Based Query Optimization (Constant folding, boolean simplification, filter pushdown).
  6. In-Memory Execution (Physical relational operator evaluation).

---

## Slide 3: Problem Statement & Technical Motivation

### Why Compiler-Style Architecture for Query Processing?
- **The Naive Approach (Interpreter Pitfall):** Simple database prototypes rely on ad-hoc regex or string splitting, resulting in brittle parsing, inability to handle operator precedence, and catastrophic performance ($O(N \times M)$ cartesian comparisons).
- **The Compiler Approach (QueryLang):**
  - **Unambiguous Grammars:** Formal EBNF parsing resolves complex nested arithmetic and logical boolean precedence.
  - **Early Semantic Verification:** Validates tables, columns, and data types at compile time before any data access occurs.
  - **Algebraic Plan Rewriting:** Compiler optimization transforms naive execution trees into provably equivalent, high-speed plans (reducing join comparisons by up to $73.3\%$).

---

## Slide 4: QueryLang DSL & Extended Language Specification

### Declarative Relational Scripting with Rich Expressions
```sql
-- 1. Core Selection and Projection
SELECT name, branch, cgpa FROM students WHERE age >= 21 ORDER BY cgpa DESC LIMIT 3;

-- 2. Multi-Table INNER JOIN with Qualified Attributes
SELECT students.name, departments.dept_name, departments.building
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.cgpa >= 8.5;

-- 3. Optimization Idiom (Constant Arithmetic & Tautologies)
SELECT students.name, departments.dept_name
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.age > (18 + 2) AND students.cgpa > 8.0 AND (1 = 1);

-- 4. Scalar Statistical Aggregations
SELECT COUNT(*), AVG(cgpa), MAX(cgpa), MIN(age), SUM(cgpa) FROM students;
```

---

## Slide 5: Formal EBNF Grammar & Operator Precedence

### 6-Level Precedence Hierarchy Without Ambiguity
```ebnf
Query            ::= "SELECT" Projection "FROM" TableReference [ JoinClause ]
                     [ "WHERE" Expression ]
                     [ "ORDER" "BY" QualifiedColumn [ "ASC" | "DESC" ] ]
                     [ "LIMIT" INTEGER ] ";"

Projection       ::= "*" | ProjectItem ( "," ProjectItem )*
ProjectItem      ::= AggregateFunction | QualifiedColumn
AggregateFunction::= ( "COUNT" "(" ( "*" | QualifiedColumn ) ")" )
                   | ( ( "SUM" | "AVG" | "MIN" | "MAX" ) "(" QualifiedColumn ")" )

Expression       ::= LogicalOrExpr
LogicalOrExpr    ::= LogicalAndExpr ( "OR" LogicalAndExpr )*
LogicalAndExpr   ::= ComparisonExpr ( "AND" ComparisonExpr )*
ComparisonExpr   ::= AdditiveExpr [ ( "=" | "!=" | ">" | "<" | ">=" | "<=" ) AdditiveExpr ]
AdditiveExpr     ::= MultiplicativeExpr ( ( "+" | "-" ) MultiplicativeExpr )*
MultiplicativeExpr::= PrimaryExpr ( ( "*" | "/" ) PrimaryExpr )*
```
- **Precedence Hierarchy:**
  `OR` (Lowest) $<$ `AND` $<$ Relational Comparisons ($=, \neq, >, <, \ge, \le$) $<$ Additive ($+, -$) $<$ Multiplicative ($*, /$) $<$ Parentheses & Atoms (Highest).

---

## Slide 6: End-to-End Compiler Pipeline Architecture

### Modular 6-Stage Compiler Flow
```
[Raw SQL Query]
       |
       v
+------------------+
| 1. Lexer         |  --> Linear token scanning with line/col tracking
+------------------+
       |
       v
+------------------+
| 2. Parser        |  --> LL(1) Recursive Descent constructs Abstract Syntax Tree (AST)
+------------------+
       |
       v
+------------------+
| 3. Semantic      |  --> Multi-schema symbol table binding & static type checking
|    Analyzer      |
+------------------+
       |
       v
+------------------+
| 4. Query Planner |  --> Generates Logical Intermediate Representation (IR) Plan
+------------------+
       |
       v
+------------------+
| 5. Optimizer     |  --> Constant Folding, Predicate Simplification, Filter Pushdown
+------------------+
       |
       v
+------------------+
| 6. Execution     |  --> Physical relational operators walk plan against in-memory data
|    Engine        |
+------------------+
       |
       v
[Tabular Output & Performance Telemetry]
```

---

## Slide 7: Front-End: Lexical Analysis & Token Scanning

### Linear Token Scanner with Precise Diagnostics
- **Single-Pass Master Regex:** Compiles 27 token specifications using `re.VERBOSE` and `re.IGNORECASE`.
- **Token Properties:** Each token maintains `TokenType`, scalar `value`, `line`, and `column` coordinate.
- **Graceful Error Recovery:** Never crashes on invalid input; captures line/column coordinates and highlights offending characters using visual ASCII caret pointers:
  ```
  [LEXICAL ERROR] at Line 1, Column 13: Invalid character sequence '@'
    --> SELECT name @ students;
                    ^
    HINT: Remove or replace the unsupported character.
  ```

---

## Slide 8: Front-End: Parser & Abstract Syntax Tree (AST)

### Strongly Typed AST Node Hierarchy
- **Recursive-Descent Parser:** Implements grammar rules as mutually recursive functions without backtrack overhead ($O(N)$ parsing time).
- **Object-Oriented AST:**
  - `SelectQueryNode`: Root AST node.
  - `TableNode` & `JoinNode`: Source and target table references.
  - `ColumnNode`: Qualified and unqualified attributes (`students.cgpa`).
  - `AggregateNode`: Aggregate invocations (`AVG(cgpa)`).
  - `ArithmeticOpNode` & `BinaryOpNode`: Expression subtrees.
  - `LiteralNode`: Terminal typed constants.
- **ASCII Tree Representation:** Every node implements `.tree_repr()` for clear inspection during compiler debugging and viva demonstrations.

---

## Slide 9: Semantic Analysis & Static Type Checking

### Multi-Schema Catalog as the Compiler Symbol Table
- **Symbol Table Structure:**
  - `SchemaCatalog`: Maintains dictionary of `TableSymbol` and `ColumnSymbol` objects.
  - Catalog schemas: `students` (5 columns) and `departments` (4 columns).
- **Four Core Semantic Verifications:**
  1. *Existence Checks:* Validates that referenced tables and columns exist in the active catalog.
  2. *Ambiguity Disambiguation:* Maps unqualified names to primary table and checks cross-table attributes.
  3. *Condition Typing:* Enforces that `WHERE` and `ON` clauses evaluate strictly to `BOOLEAN`.
  4. *Type Compatibility:* Static type verification on comparisons (e.g., rejecting `STRING > INTEGER`) and arithmetic operations (requiring numeric types).

---

## Slide 10: Intermediate Representation: Relational Algebra IR

### Lowering Declarative AST into Operator Plans
- **Relational Algebra Mapping:**
  - Sequential Scan: $\text{SCAN}(R)$ (`ScanNode`)
  - Relational Selection: $\sigma_{\theta}(R)$ (`FilterNode`)
  - Relational Projection: $\pi_{c_1, \dots, c_k}(R)$ (`ProjectNode`)
  - Relational Inner Join: $R \bowtie_{\psi} S$ (`JoinPlanNode`)
  - Statistical Aggregation: $\gamma_{f_1, \dots, f_m}(R)$ (`AggregatePlanNode`)
  - Ordering & Truncation: $\tau_{c}(R)$ (`SortNode`), $\lambda_{k}(R)$ (`LimitNode`)
- **IR Independence:** The execution plan is cleanly decoupled from source syntax, allowing algebraic rewrites to occur in the middle-end before physical execution.

---

## Slide 11: Rule-Based Optimizer: Constant Folding & Simplification

### Compile-Time Static Evaluation & Boolean Reductions
- **Constant Folding (`ConstantFolder`):**
  - Recursively evaluates arithmetic trees of literal constants:
    $$\text{Fold}((18 + 2) * 1) \to 20$$
  - Statically evaluates literal comparisons:
    $$(1 = 1) \to \text{TRUE}$$
- **Predicate Simplification (`PredicateSimplifier`):**
  - Applies boolean algebraic axioms:
    $$\phi \land \text{TRUE} \implies \phi \quad (\text{Identity})$$
    $$\phi \land \text{FALSE} \implies \text{FALSE} \quad (\text{Annihilation})$$
  - Redundant filter elimination: If predicate reduces to constant $\text{TRUE}$, the filter operator is pruned from the plan tree entirely.

---

## Slide 12: Rule-Based Optimizer: Algebraic Filter Pushdown

### Minimizing Intermediate Join Cardinality
- **The Optimization Theorem:**
  $$\pi(\sigma_{\theta}(R \bowtie S)) \equiv \pi((\sigma_{\theta}(R)) \bowtie S) \quad \text{if } \text{attrs}(\theta) \subseteq \text{schema}(R)$$
- **Plan Transformation Before & After:**
  ```
  [UNOPTIMIZED PLAN]                     [OPTIMIZED PLAN]
  PROJECT [name, dept_name]             PROJECT [name, dept_name]
    \-- FILTER [age > 20]                 \-- JOIN [ON branch = dept_name]
        \-- JOIN [ON branch = dept_name]        |-- FILTER [age > 20]  <-- PUSHED DOWN!
            |-- SCAN [students]                 |   \-- SCAN [students]
            \-- SCAN [departments]              \-- SCAN [departments]
  ```
- **Cardinally Reduction:** Filters out non-matching rows *before* entering the join, avoiding expensive pairwise evaluation on discarded records.

---

## Slide 13: Language Extensions: Relational JOIN & Aggregates

### Advanced Relational Capabilities
- **Multi-Table Relational INNER JOIN:**
  - Evaluates cross-table equi-join conditions (`students.branch = departments.dept_name`).
  - Supports qualified column selection across both primary and joined schemas (`students.name`, `departments.building`).
- **Scalar Statistical Aggregations:**
  - Implements `COUNT(*)`, `COUNT(col)`, `AVG(col)`, `SUM(col)`, `MIN(col)`, `MAX(col)`.
  - Computes summary statistics over filtered datasets in a single streaming pass ($O(N)$ time, $O(1)$ space).
  - Clean tabular output formatted with aligned ASCII borders.

---

## Slide 14: Execution Engine & Empirical Benchmarks

### Verified Execution Speedups on Synthetic Datasets
- **Benchmark Query:**
  ```sql
  SELECT students.name, departments.dept_name
  FROM students JOIN departments ON students.branch = departments.dept_name
  WHERE students.age > (18 + 2) AND students.cgpa > 8.0;
  ```
- **Empirical Execution Timings:**

  | Record Scale ($N$) | Unoptimized Plan | Optimized Plan | Speedup Ratio | Join Comparisons Saved |
  |:---:|:---:|:---:|:---:|:---:|
  | **100 rows** | 4.615 ms | 2.442 ms | **$1.89\times$** | $73.0\%$ |
  | **1,000 rows** | 48.331 ms | 25.017 ms | **$1.93\times$** | $70.5\%$ |
  | **10,000 rows** | 504.321 ms | 220.880 ms | **$2.28\times$** | **$73.3\%$** |

- **Verification:** Both plans return 100% identical result sets across all scales.

---

## Slide 15: Formal Quality Assurance: 25-Point Verification Matrix

### 100% Pass Rate Across All Compiler Phases
- **25 Formal Verification Tests (T-01 to T-25):**
  - $\text{T-01}$ to $\text{T-08}$: Basic projections, compound filters, sorting, limits (**PASS**)
  - $\text{T-09}$ to $\text{T-15}$: Lexical, syntax, semantic, type errors & boundaries (**PASS**)
  - $\text{T-16}$: 6-stage end-to-end compiler inspection (**PASS**)
  - $\text{T-17}$ to $\text{T-19}$: Constant folding, predicate simplification, filter pushdown (**PASS**)
  - $\text{T-20}$ to $\text{T-21}$: Multi-table inner joins & qualified column resolution (**PASS**)
  - $\text{T-22}$ to $\text{T-23}$: Scalar aggregations (`COUNT`, `AVG`, `MAX`, `MIN`, `SUM`) (**PASS**)
  - $\text{T-24}$ to $\text{T-25}$: Arithmetic in WHERE conditions & Graphviz DOT export (**PASS**)
- **Unit Test Suite:** 26 / 26 PyUnit unit tests pass with 0 errors and 0 failures.

---

## Slide 16: Conclusion, Viva Summary & Future Roadmap

### Summary of Achievements
- Successfully built **QueryLang**, a full compiler-style relational query engine conforming strictly to all Review 1, 2, and 3 rubrics.
- Demonstrated genuine compiler concepts: lexical scanning, recursive descent, AST pretty-printing, symbol table typing, intermediate relational plans, algebraic optimization rewrites, and physical operator walking.
- **Future Roadmap:**
  1. Cost-Based Optimization (CBO) using histogram statistics.
  2. Bytecode Virtual Machine (VDBE) code generation.
  3. Persistent B+Tree storage manager on disk.

*Thank you! Ready for Viva Questions & Live Demonstration.*
