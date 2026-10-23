"""
Script to build high-quality downloadable presentation slides PDF and progress report PDF
for QueryLang Review 3 (Final Project Review) using Microsoft Edge headless PDF rendering.
"""

import os
import sys
import subprocess
import shutil

DESKTOP_DIR = r"c:\Users\amank\OneDrive\Desktop"
PROJECT_DIR = os.path.join(DESKTOP_DIR, "QueryLang")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def generate_presentation_html() -> str:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>QueryLang Review 3 Final Presentation</title>
<style>
  @page {
    size: 16in 9in;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background: #f8fafc;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .slide {
    width: 16in;
    height: 9in;
    position: relative;
    padding: 0.75in 1.1in 0.65in 1.1in;
    background: #ffffff;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .slide-header {
    margin-bottom: 0.3in;
  }
  .slide-title {
    font-size: 32pt;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.5px;
  }
  .slide-subtitle {
    font-size: 15pt;
    color: #64748b;
    margin-top: 4px;
    font-weight: 500;
  }
  .slide-footer {
    position: absolute;
    bottom: 0.35in;
    left: 1.1in;
    right: 1.1in;
    border-top: 1.5px solid #cbd5e1;
    padding-top: 8px;
    display: flex;
    justify-content: space-between;
    font-size: 11pt;
    color: #64748b;
  }
  .slide-number {
    font-weight: 600;
    color: #334155;
  }
  .content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  .columns-2 {
    display: flex;
    gap: 0.5in;
    flex: 1;
  }
  .col {
    flex: 1;
  }
  .card {
    background: #f8fafc;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.22in 0.3in;
    margin-bottom: 0.18in;
  }
  .card-title {
    font-size: 16pt;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 8px;
  }
  p, li {
    font-size: 13.5pt;
    line-height: 1.45;
    color: #334155;
  }
  ul {
    margin-left: 20px;
    margin-top: 6px;
  }
  li {
    margin-bottom: 6px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5pt;
    margin-top: 8px;
  }
  th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 9px 12px;
    border-bottom: 2px solid #cbd5e1;
  }
  td {
    padding: 8px 12px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
  }
  tr:nth-child(even) td {
    background: #f8fafc;
  }
  .badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 10.5pt;
    font-weight: 700;
  }
  .badge-pass { background: #dcfce7; color: #15803d; }
  .badge-blue { background: #dbeafe; color: #1d4ed8; }
  .badge-purple { background: #f3e8ff; color: #7e22ce; }
  .badge-amber { background: #fef3c7; color: #b45309; }
  pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 12px 16px;
    border-radius: 8px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 11pt;
    line-height: 1.35;
    overflow-x: hidden;
    white-space: pre-wrap;
  }
  code {
    font-family: "Consolas", monospace;
    background: #e2e8f0;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 12pt;
  }
  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
  }
  .title-slide {
    justify-content: center;
    align-items: center;
    text-align: center;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
  }
  .title-tag {
    display: inline-block;
    padding: 6px 16px;
    background: #2563eb;
    color: #ffffff;
    font-weight: 700;
    border-radius: 20px;
    font-size: 14pt;
    letter-spacing: 1px;
    margin-bottom: 20px;
  }
  .main-title {
    font-size: 42pt;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 12px;
    letter-spacing: -1px;
  }
  .sub-title {
    font-size: 20pt;
    color: #94a3b8;
    max-width: 12in;
    margin-bottom: 40px;
    line-height: 1.35;
  }
  .meta-box {
    display: flex;
    gap: 0.8in;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 18px 40px;
    text-align: left;
  }
  .meta-item-label {
    font-size: 11pt;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
  .meta-item-val {
    font-size: 15pt;
    color: #f8fafc;
    font-weight: 600;
  }
</style>
</head>
<body>

<!-- SLIDE 1: TITLE SLIDE -->
<div class="slide title-slide">
  <div class="title-tag">BCSE307P COMPILER DESIGN LABORATORY &bull; REVIEW 3 FINAL</div>
  <div class="main-title">QueryLang: A Compiler-Style Query Engine<br>with Rule-Based Query Optimization</div>
  <div class="sub-title">Design, Formal Verification, and Empirical Benchmarking of a Domain-Specific Relational Compiler</div>
  
  <div class="meta-box">
    <div>
      <div class="meta-item-label">Student Candidate</div>
      <div class="meta-item-val">Aman Katakwar (24BCE0160)</div>
    </div>
    <div>
      <div class="meta-item-label">Faculty Guide</div>
      <div class="meta-item-val">Prof. Ranjithkumar S</div>
    </div>
    <div>
      <div class="meta-item-label">School / Institution</div>
      <div class="meta-item-val">SCOPE, VIT Vellore</div>
    </div>
    <div>
      <div class="meta-item-label">Evaluation Phase</div>
      <div class="meta-item-val">Review 3 / Final Viva</div>
    </div>
  </div>
</div>

<!-- SLIDE 2: EXECUTIVE SUMMARY -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">1. Executive Summary & Vision</div>
    <div class="slide-subtitle">Demonstrating genuine compiler construction paradigms on declarative query languages</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Industrial Rationale: DBMS as Compilers</div>
          <p>Contemporary relational engines (SQLite, DuckDB, PostgreSQL) are <strong>domain-specific compilers</strong>. They do not interpret raw query strings; they parse, semantically validate, translate to Intermediate Representation (IR), optimize algebraically, and walk physical operator plans.</p>
          <ul>
            <li><strong>Declarative Abstraction:</strong> Queries specify <em>what</em> data is desired, leaving the compiler to construct the <em>optimal execution strategy</em>.</li>
            <li><strong>Compilation Rigor:</strong> Lexical scanning, LL(1) recursive descent, typed ASTs, symbol table catalog binding, and algebraic rewrites.</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title">Scope of Review 3 Delivery</div>
          <p>All planned Phase 3 milestones fully realized from first principles using standard Python 3.12 (Zero third-party dependencies):</p>
          <ul>
            <li>Rule-based Query Optimizer (Constant Folding, Predicate Simplification, Filter Pushdown).</li>
            <li>Multi-table relational <code>INNER JOIN</code> with qualified attributes.</li>
            <li>Scalar Aggregations (<code>COUNT</code>, <code>AVG</code>, <code>SUM</code>, <code>MIN</code>, <code>MAX</code>).</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Key Engineering Achievements</div>
          <table>
            <tr><th>Metric / Phase</th><th>Status / Verified Achievement</th></tr>
            <tr><td><strong>Grammar Precedence</strong></td><td>6-tier unambiguous hierarchy (Boolean &lt; Comparison &lt; Arithmetic)</td></tr>
            <tr><td><strong>Optimizer Rules</strong></td><td>Constant Folding, Tautology Simplification, Join Filter Pushdown</td></tr>
            <tr><td><strong>Benchmark Speedup</strong></td><td><strong>1.89x to 2.28x speedup</strong> on 100, 1k, and 10k synthetic datasets</td></tr>
            <tr><td><strong>Test Matrix</strong></td><td><strong>25 / 25 formal tests PASS (100%)</strong> + 26 PyUnit unit tests</td></tr>
            <tr><td><strong>Visualizer</strong></td><td>Graphviz DOT export for AST and Relational Plans</td></tr>
          </table>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 2 / 16</span>
  </div>
</div>

<!-- SLIDE 3: PROBLEM STATEMENT -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">2. Problem Statement & Motivation</div>
    <div class="slide-subtitle">Overcoming naive interpreter bottlenecks through formal compiler pipeline design</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">The Naive Interpreter Pitfall</div>
          <ul>
            <li><strong>Regex / String Splitting:</strong> Brittle, cannot handle nested parentheses, multi-level operator precedence, or string escapes.</li>
            <li><strong>Late Semantic Binding:</strong> Errors (unknown columns, type mismatches) surface mid-execution rather than at compile time.</li>
            <li><strong>Cartesian Join Explosions:</strong> Joins without filter pushdown execute full cartesian products: \(O(N \times M)\) comparisons.</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title">The QueryLang Solution</div>
          <p>A decoupled 6-phase compiler pipeline guaranteeing:</p>
          <ul>
            <li><strong>Deterministic Parsing:</strong> Clean LL(1) grammar without left recursion.</li>
            <li><strong>Compile-Time Safety:</strong> Static type checking and catalog binding before data evaluation.</li>
            <li><strong>Algebraic Minimization:</strong> Filter pushdown reduces join inputs from \(N \times M\) to \(\sigma(N) \times M\).</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Execution Complexity Contrast</div>
          <pre>
-- Query with Join & Filter:
SELECT s.name, d.dept_name FROM students s 
JOIN departments d ON s.branch = d.dept_name 
WHERE s.age > 20;

[NAIVE / UNOPTIMIZED EXECUTION]
Step 1: Nested Loop Join: N * M iterations = 10,000 * 5 = 50,000 comparisons
Step 2: Filter applied after join over all 50,000 candidate records.

[QUERYLANG OPTIMIZED EXECUTION (FILTER PUSHDOWN)]
Step 1: Filter pushed to SCAN[students]: 10,000 * 0.267 = 2,672 rows
Step 2: Join executed on filtered subset: 2,672 * 5 = 13,360 comparisons
RESULT: 73.3% reduction in join comparisons!</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 3 / 16</span>
  </div>
</div>

<!-- SLIDE 4: DSL SPECIFICATION -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">3. QueryLang DSL & Extended Language Specification</div>
    <div class="slide-subtitle">Declarative SQL dialect supporting relational selections, joins, arithmetic, and aggregates</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Core Language Features</div>
          <ul>
            <li><strong>Projections:</strong> Column lists (<code>name, cgpa</code>), wildcard (<code>*</code>), and qualified identifiers (<code>students.name</code>).</li>
            <li><strong>Multi-Table Joins:</strong> Explicit <code>[INNER] JOIN ... ON &lt;condition&gt;</code> syntax.</li>
            <li><strong>Aggregations:</strong> <code>COUNT(*)</code>, <code>COUNT(col)</code>, <code>AVG</code>, <code>SUM</code>, <code>MIN</code>, <code>MAX</code>.</li>
            <li><strong>Arithmetic Expressions:</strong> Full arithmetic support (<code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>( )</code>) in conditions.</li>
            <li><strong>Ordering & Limits:</strong> <code>ORDER BY &lt;col&gt; [ASC|DESC]</code> and <code>LIMIT &lt;int&gt;</code>.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Representative Canonical Queries</div>
          <pre>
-- 1. Selection, Projection, Ordering, Limit
SELECT name, branch, cgpa FROM students 
WHERE age >= 21 ORDER BY cgpa DESC LIMIT 3;

-- 2. Multi-Table INNER JOIN with Qualified Attributes
SELECT students.name, departments.dept_name, departments.building
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.cgpa >= 8.5;

-- 3. Optimization Idiom (Constant Folding + Filter Pushdown)
SELECT students.name, departments.dept_name
FROM students
JOIN departments ON students.branch = departments.dept_name
WHERE students.age > (18 + 2) AND (1 = 1);

-- 4. Statistical Aggregations
SELECT COUNT(*), AVG(cgpa), MAX(cgpa), MIN(age) FROM students;</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 4 / 16</span>
  </div>
</div>

<!-- SLIDE 5: FORMAL EBNF GRAMMAR -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">4. Formal EBNF Grammar & Precedence Hierarchy</div>
    <div class="slide-subtitle">Strict, unambiguous grammar resolving boolean, relational, and arithmetic precedence</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Operator Precedence Hierarchy</div>
          <table>
            <tr><th>Level</th><th>Operators</th><th>Associativity</th></tr>
            <tr><td><strong>1 (Lowest)</strong></td><td><code>OR</code></td><td>Left-to-Right</td></tr>
            <tr><td><strong>2</strong></td><td><code>AND</code></td><td>Left-to-Right</td></tr>
            <tr><td><strong>3</strong></td><td><code>=</code>, <code>!=</code>, <code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code></td><td>Non-associative</td></tr>
            <tr><td><strong>4</strong></td><td><code>+</code>, <code>-</code></td><td>Left-to-Right</td></tr>
            <tr><td><strong>5</strong></td><td><code>*</code>, <code>/</code></td><td>Left-to-Right</td></tr>
            <tr><td><strong>6 (Highest)</strong></td><td><code>( ... )</code>, Identifiers, Literals</td><td>Unary / Atom</td></tr>
          </table>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Grammar Specification (EBNF Snippet)</div>
          <pre>
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
MultiplicativeExpr::= PrimaryExpr ( ( "*" | "/" ) PrimaryExpr )*</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 5 / 16</span>
  </div>
</div>

<!-- SLIDE 6: COMPILER ARCHITECTURE -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">5. End-to-End Compiler Pipeline Architecture</div>
    <div class="slide-subtitle">Modular 6-stage compiler lowering queries from high-level text to optimized execution</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Pipeline Stages & Module Responsibilities</div>
          <ul>
            <li><strong>Stage 1: Lexical Analysis (<code>lexer/</code>):</strong> Converts raw query text into token stream with coordinates.</li>
            <li><strong>Stage 2: Syntax Analysis (<code>parser/</code>):</strong> LL(1) recursive descent builds typed AST.</li>
            <li><strong>Stage 3: Semantic Analysis (<code>semantic/</code>):</strong> Multi-schema catalog symbol binding & type inference.</li>
            <li><strong>Stage 4: Query Planner (<code>planner/</code>):</strong> Emits Relational Algebra Logical Plan (IR).</li>
            <li><strong>Stage 5: Query Optimizer (<code>optimizer/</code>):</strong> Constant folding, simplification & filter pushdown.</li>
            <li><strong>Stage 6: Execution Engine (<code>execution/</code>):</strong> Evaluates optimized plan over in-memory relation data.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Compiler Architecture Diagram</div>
          <pre>
[Raw SQL Query]
       |
       v
+------------------+
| 1. Lexer         |  --> Emits Token Stream with line/col tracking
+------------------+
       |
       v
+------------------+
| 2. Parser        |  --> Constructs Abstract Syntax Tree (AST)
+------------------+
       |
       v
+------------------+
| 3. Semantic      |  --> Schema Catalog Symbol Binding & Type Checking
|    Analyzer      |
+------------------+
       |
       v
+------------------+
| 4. Query Planner |  --> Lowers AST to Relational Algebra IR
+------------------+
       |
       v
+------------------+
| 5. Optimizer     |  --> Constant Folding, Simplification, Filter Pushdown
+------------------+
       |
       v
+------------------+
| 6. Execution     |  --> Physical Relational Operators on Memory Tables
|    Engine        |
+------------------+
       |
       v
[Tabular Output & Execution Diagnostics]</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 6 / 16</span>
  </div>
</div>

<!-- SLIDE 7: LEXICAL ANALYSIS -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">6. Front-End: Lexical Analysis & Token Scanning</div>
    <div class="slide-subtitle">Linear-time scanning with 27 token types and coordinate-aware diagnostic recovery</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Scanner Architecture (<code>lexer/lexer.py</code>)</div>
          <ul>
            <li><strong>Single Linear Pass:</strong> Master regex compiled with <code>re.VERBOSE</code> and <code>re.IGNORECASE</code>.</li>
            <li><strong>Token Representation:</strong> Each <code>Token</code> records <code>TokenType</code>, literal value, source line, and column position.</li>
            <li><strong>Review 3 Token Extensions:</strong>
              <ul>
                <li>Keywords: <code>JOIN</code>, <code>INNER</code>, <code>ON</code>, <code>COUNT</code>, <code>SUM</code>, <code>AVG</code>, <code>MIN</code>, <code>MAX</code>.</li>
                <li>Operators: <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>.</code> (DOT for qualified attributes).</li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Lexical Error Diagnostic Output</div>
          <pre>
[LEXICAL ERROR] at Line 1, Column 13: Invalid character sequence '@'
  --> SELECT name @ students;
                  ^
  HINT: Remove or replace the unsupported character.

Token Stream Sample:
  Token(SELECT, line=1, col=1)
  Token(IDENTIFIER, 'name', line=1, col=8)
  Token(COMMA, line=1, col=12)
  Token(IDENTIFIER, 'branch', line=1, col=14)
  Token(FROM, line=1, col=21)
  Token(IDENTIFIER, 'students', line=1, col=26)
  Token(SEMICOLON, line=1, col=34)
  Token(EOF, line=1, col=35)</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 7 / 16</span>
  </div>
</div>

<!-- SLIDE 8: SYNTAX ANALYSIS & AST -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">7. Front-End: Syntax Analysis & AST Construction</div>
    <div class="slide-subtitle">LL(1) recursive-descent parser producing strongly typed, hierarchical syntax trees</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Parser Architecture (<code>parser/parser.py</code>)</div>
          <ul>
            <li><strong>Deterministic LL(1):</strong> Single-token lookahead without backtracking overhead (\(O(N)\) parsing time).</li>
            <li><strong>AST Node Hierarchy (<code>ast/nodes.py</code>):</strong>
              <ul>
                <li><code>SelectQueryNode</code>: Complete query representation.</li>
                <li><code>TableNode</code> & <code>JoinNode</code>: Source relations and joins.</li>
                <li><code>ColumnNode</code>: Qualified / unqualified column refs.</li>
                <li><code>AggregateNode</code>: Statistical aggregate expressions.</li>
                <li><code>ArithmeticOpNode</code> & <code>BinaryOpNode</code>: Expression trees.</li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Generated AST Tree Representation</div>
          <pre>
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
\-- LIMIT: 3</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 8 / 16</span>
  </div>
</div>

<!-- SLIDE 9: SEMANTIC ANALYSIS -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">8. Semantic Analysis & Multi-Schema Symbol Binding</div>
    <div class="slide-subtitle">Cross-schema catalog validation, column disambiguation, and static type checking</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Schema Catalog as Symbol Table</div>
          <p>Maintains table symbols and column symbol dictionaries across all active relations:</p>
          <ul>
            <li><code>students</code> (id:INT, name:STR, age:INT, branch:STR, cgpa:FLOAT)</li>
            <li><code>departments</code> (dept_id:INT, dept_name:STR, hod:STR, building:STR)</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title">Static Type Checking Rules</div>
          <ul>
            <li><strong>Comparisons:</strong> Rejects incompatible operands (e.g., <code>STRING &gt; INTEGER</code>).</li>
            <li><strong>Arithmetic:</strong> Enforces numeric operands (<code>INTEGER</code> or <code>FLOAT</code>).</li>
            <li><strong>Aggregates:</strong> Restricts <code>SUM</code> and <code>AVG</code> strictly to numeric columns.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Semantic Diagnostic Examples</div>
          <pre>
-- Unknown Column Error:
[SEMANTIC ERROR] at Line 1, Column 8: 
Column 'salary' does not exist in table 'students'.
  --> SELECT salary FROM students;
             ^
  HINT: Available columns: id, name, age, branch, cgpa

------------------------------------------------
-- Static Type Mismatch Error:
[SEMANTIC ERROR] at Line 1, Column 38: 
Operator '>' cannot be applied to STRING and INTEGER.
  --> SELECT name FROM students WHERE name > 50;
                                           ^
  HINT: Relational ordering requires compatible types.</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 9 / 16</span>
  </div>
</div>

<!-- SLIDE 10: INTERMEDIATE REPRESENTATION -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">9. Relational Algebra Intermediate Representation (IR)</div>
    <div class="slide-subtitle">Lowering decorated ASTs into decoupled relational algebra operator trees</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Relational Operators (<code>planner/plan.py</code>)</div>
          <ul>
            <li><code>ScanNode</code>: Base relation access: \(\text{SCAN}(R)\).</li>
            <li><code>JoinPlanNode</code>: Inner join operator: \(R \bowtie_{\theta} S\).</li>
            <li><code>FilterNode</code>: Relational selection: \(\sigma_{\theta}(R)\).</li>
            <li><code>ProjectNode</code>: Relational projection: \(\pi_{c_1, \dots, c_k}(R)\).</li>
            <li><code>AggregatePlanNode</code>: Statistical aggregation: \(\gamma_{f_1, \dots, f_m}(R)\).</li>
            <li><code>SortNode</code> & <code>LimitNode</code>: Ordering \(\tau_{c}(R)\) and truncation \(\lambda_{k}(R)\).</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Generated Logical Plan Tree (IR)</div>
          <pre>
\-- LIMIT [3]
    \-- SORT [cgpa DESC]
        \-- PROJECT [name, branch, cgpa]
            \-- FILTER [age >= (18 + 2) AND (1 = 1)]
                \-- SCAN [students]

Formal Relational Algebra Expression:
&lambda;_{3} ( &tau;_{cgpa DESC} ( &pi;_{name, branch, cgpa} ( 
    &sigma;_{age &ge; 20} ( SCAN(students) ) 
) ) )</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 10 / 16</span>
  </div>
</div>

<!-- SLIDE 11: RULE-BASED OPTIMIZER -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">10. Rule-Based Query Optimizer: Constant Folding & Simplification</div>
    <div class="slide-subtitle">Compile-time static evaluation and boolean algebraic reductions</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Optimization Rule 1: Constant Folding</div>
          <p>Recursively pre-computes constant arithmetic and comparisons at compile time:</p>
          <ul>
            <li>\(\text{Fold}((18 + 2)) \to 20\)</li>
            <li>\(\text{Fold}(1 = 1) \to \text{TRUE}\)</li>
            <li>Eliminates repeated runtime arithmetic inside per-row execution loops.</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title">Optimization Rule 2: Predicate Simplification</div>
          <p>Applies classical boolean algebraic axioms:</p>
          <ul>
            <li><strong>Identity:</strong> \(P \land \text{TRUE} \implies P\)</li>
            <li><strong>Annihilation:</strong> \(P \land \text{FALSE} \implies \text{FALSE}\)</li>
            <li><strong>Filter Elimination:</strong> Constant \(\text{TRUE}\) filters pruned entirely.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Optimizer Transformation Report</div>
          <pre>
=== QUERY OPTIMIZATION REPORT ===
Rules Applied:
  [x] Constant Folding: folded 2 static expression(s)
  [x] Predicate Simplification: simplified 1 redundant term(s)

--- ORIGINAL PLAN ---
\-- PROJECT [name, branch, cgpa]
    \-- FILTER [age >= (18 + 2) AND (1 = 1)]
        \-- SCAN [students]

--- OPTIMIZED PLAN ---
\-- PROJECT [name, branch, cgpa]
    \-- FILTER [age >= 20]
        \-- SCAN [students]</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 11 / 16</span>
  </div>
</div>

<!-- SLIDE 12: FILTER PUSHDOWN -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">11. Rule-Based Query Optimizer: Algebraic Filter Pushdown</div>
    <div class="slide-subtitle">Relocating selection operators past relational joins to minimize intermediate cardinality</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Algebraic Equivalence Theorem</div>
          <p>If selection predicate \(\theta\) references attributes strictly from relation \(R\):</p>
          <p style="text-align:center; font-weight:700; margin: 10px 0; font-size: 14pt;">
            \(\pi(\sigma_{\theta}(R \bowtie_{\psi} S)) \equiv \pi((\sigma_{\theta}(R)) \bowtie_{\psi} S)\)
          </p>
          <ul>
            <li><strong>Cardinality Reduction:</strong> Filters rows <em>before</em> the join rather than after.</li>
            <li><strong>Join Pruning:</strong> Drops non-qualifying tuples immediately, saving nested-loop comparisons.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Before vs. After Plan Comparison</div>
          <pre>
--- ORIGINAL PLAN (FILTER AFTER JOIN) ---
\-- PROJECT [name, dept_name]
    \-- FILTER [students.age > 20]
        \-- JOIN [ON students.branch = departments.dept_name]
            |-- SCAN [students]
            \-- SCAN [departments]

--- OPTIMIZED PLAN (FILTER PUSHED DOWN) ---
\-- PROJECT [name, dept_name]
    \-- JOIN [ON students.branch = departments.dept_name]
        |-- FILTER [students.age > 20]  <-- PUSHED TO SCAN!
        |   \-- SCAN [students]
        \-- SCAN [departments]</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 12 / 16</span>
  </div>
</div>

<!-- SLIDE 13: JOINS AND AGGREGATES -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">12. Language Extensions: Multi-Table JOIN & Aggregates</div>
    <div class="slide-subtitle">Cross-relation equi-joins and streaming scalar statistical aggregations</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Multi-Table Relational INNER JOIN</div>
          <pre>
SELECT s.name, d.dept_name, d.building
FROM students s JOIN departments d 
ON s.branch = d.dept_name 
WHERE s.cgpa >= 8.5;

+--------+-----------+------------------+
| NAME   | DEPT_NAME | BUILDING         |
+--------+-----------+------------------+
| Asha   | CSE       | Technology Tower |
| Rahul  | CSE       | Technology Tower |
| Ananya | CSE       | Technology Tower |
+--------+-----------+------------------+
3 row(s) in set (Scanned: 10, Filtered: 4)</pre>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Scalar Statistical Aggregations</div>
          <pre>
SELECT COUNT(*), AVG(cgpa), MAX(cgpa), MIN(age) 
FROM students;

+----------+-----------+-----------+----------+
| COUNT(*) | AVG(CGPA) | MAX(CGPA) | MIN(AGE) |
+----------+-----------+-----------+----------+
| 7        | 8.43      | 9.4       | 19       |
+----------+-----------+-----------+----------+
1 row(s) in set (Scanned: 7, Filtered: 0)

Complexity: Single streaming pass O(N) time,
O(1) auxiliary accumulator memory.</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 13 / 16</span>
  </div>
</div>

<!-- SLIDE 14: BENCHMARKS -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">13. In-Memory Execution Engine & Performance Benchmarks</div>
    <div class="slide-subtitle">Empirical validation of optimization speedups across 100, 1,000, and 10,000 synthetic rows</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Empirical Benchmark Results Table</div>
          <table>
            <tr><th>Rows (N)</th><th>Unoptimized</th><th>Optimized</th><th>Speedup</th><th>Equivalence</th></tr>
            <tr><td><strong>100</strong></td><td>4.615 ms</td><td>2.442 ms</td><td><span class="badge badge-pass">1.89x</span></td><td>100% Match</td></tr>
            <tr><td><strong>1,000</strong></td><td>48.331 ms</td><td>25.017 ms</td><td><span class="badge badge-pass">1.93x</span></td><td>100% Match</td></tr>
            <tr><td><strong>10,000</strong></td><td>504.321 ms</td><td>220.880 ms</td><td><span class="badge badge-pass">2.28x</span></td><td>100% Match</td></tr>
          </table>
        </div>
        <div class="card">
          <div class="card-title">Complexity Analysis</div>
          <ul>
            <li><strong>Constant Folding:</strong> Precomputed static arithmetic eliminates 10,000 runtime additions.</li>
            <li><strong>Filter Pushdown:</strong> Input to join cut from 10k to 2,672 rows, saving 36,640 pairwise checks.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Benchmark Telemetry Output</div>
          <pre>
==============================================================
QUERYLANG BENCHMARK: UNOPTIMIZED vs. OPTIMIZED IR
==============================================================
Query:
  SELECT students.name, departments.dept_name
  FROM students JOIN departments 
  ON students.branch = departments.dept_name
  WHERE students.age > (18 + 2) AND students.cgpa > 8.0;

Rules Applied:
  [x] Constant Folding: folded 1 static expression
  [x] Filter Pushdown: pushed filter to SCAN[students]

Observations:
1. Average speedup exceeds 2.0x on large datasets.
2. Verified 100% result equivalence across all runs.</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 14 / 16</span>
  </div>
</div>

<!-- SLIDE 15: VERIFICATION MATRIX -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">14. Formal Quality Assurance: 25-Point Verification Matrix</div>
    <div class="slide-subtitle">100% test pass rate across all compiler phases, optimizations, and language extensions</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Formal Verification Matrix (T-01 to T-25)</div>
          <table>
            <tr><th>IDs</th><th>Category</th><th>Verified Feature</th><th>Status</th></tr>
            <tr><td><strong>T-01 - T-03</strong></td><td>Projections</td><td>Basic, Multi-column, Relational Filter</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-04 - T-06</strong></td><td>Compound</td><td>AND, OR, Wildcard (*) Selection</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-07 - T-08</strong></td><td>Ordering</td><td>ORDER BY ASC/DESC, LIMIT Truncation</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-09 - T-11</strong></td><td>Front-End</td><td>Lexical Error, Missing Col, Missing FROM</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-12 - T-15</strong></td><td>Semantics</td><td>Unknown Table, Unknown Col, Type Error</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-16</strong></td><td>Pipeline</td><td>6-Stage Full Compiler Inspection</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-17 - T-19</strong></td><td>Optimizer</td><td>Constant Folding, Simplification, Pushdown</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-20 - T-21</strong></td><td>Joins</td><td>Multi-Table INNER JOIN, Qualified Col</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-22 - T-23</strong></td><td>Aggregates</td><td>COUNT(*), AVG, MAX, MIN, SUM</td><td><span class="badge badge-pass">PASS</span></td></tr>
            <tr><td><strong>T-24 - T-25</strong></td><td>Expressions</td><td>Arithmetic in WHERE, Graphviz DOT</td><td><span class="badge badge-pass">PASS</span></td></tr>
          </table>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Automated Test Runner Output</div>
          <pre>
====================================================================================
      QUERYLANG COMPILER ENGINE - REVIEW 3 FINAL VERIFICATION MATRIX
====================================================================================
Total Verification Matrix Tests: 25 | Passed: 25 | Failed: 0
Verification Status: 100% PASS RATE

Running Formal PyUnit Test Suites...
test_basic_tokenization (test_lexer.TestLexer) ... ok
test_invalid_character_error (test_lexer.TestLexer) ... ok
test_syntax_error_missing_column (test_parser.TestParser) ... ok
test_semantic_error_type_mismatch (test_semantic.TestSemanticAnalyzer) ... ok
test_constant_folding (test_optimizer.TestOptimizerAndExtensions) ... ok
test_filter_pushdown_past_join (test_optimizer.TestOptimizerAndExtensions) ... ok
test_relational_join_execution (test_optimizer.TestOptimizerAndExtensions) ... ok
test_aggregates_execution (test_optimizer.TestOptimizerAndExtensions) ... ok
----------------------------------------------------------------------
Ran 26 tests in 0.011s -- OK</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 15 / 16</span>
  </div>
</div>

<!-- SLIDE 16: CONCLUSION & ROADMAP -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">15. Conclusion, Viva Defense & Engineering Roadmap</div>
    <div class="slide-subtitle">Summary of completed compiler milestones and future research directions</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Summary of Achievements</div>
          <ul>
            <li><strong>Complete 6-Phase Pipeline:</strong> Lexer $\to$ Parser $\to$ Semantic Analyzer $\to$ Planner $\to$ Optimizer $\to$ Engine.</li>
            <li><strong>Genuine Compiler Implementation:</strong> First-principles Python standard library without external regex or parser generator shortcuts.</li>
            <li><strong>Algebraic Optimizer:</strong> Proven speedups of up to 2.28x on 10,000 synthetic rows via constant folding and filter pushdown.</li>
            <li><strong>Deliverables:</strong> 21-Chapter Report, 16-Slide Presentation Deck, interactive CLI, and downloadable PDFs.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Future Engineering Roadmap</div>
          <ul>
            <li><strong>Cost-Based Optimization (CBO):</strong> Using catalog histogram statistics to choose optimal join orderings.</li>
            <li><strong>Bytecode Virtual Machine (VDBE):</strong> Lowering relational plans to stack/register bytecode to eliminate interpreter overhead.</li>
            <li><strong>Persistent Storage Engine:</strong> Implementing a slotted-page buffer pool manager and disk-based B+Tree index.</li>
          </ul>
          <div style="margin-top: 25px; padding: 15px; background: #e0f2fe; border-radius: 8px; border: 1px solid #7dd3fc; text-align: center;">
            <p style="font-size: 15pt; font-weight: 700; color: #0369a1;">Thank you! Ready for Viva Questions & Live Demonstration.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 3 Final Project Review</span>
    <span class="slide-number">Slide 16 / 16</span>
  </div>
</div>

</body>
</html>
"""
    return html


def generate_report_html() -> str:
    # Read the markdown report or generate formal HTML
    # We will build a structured, beautifully styled A4 report matching REVIEW_3_REPORT.md
    with open(os.path.join(PROJECT_DIR, "REVIEW_3_REPORT.md"), "r", encoding="utf-8") as f:
        md_text = f.read()

    # Simple markdown-to-HTML conversion tailored for our 21 chapters
    import html as html_lib

    lines = md_text.splitlines()
    body_html = []
    in_table = False
    in_pre = False
    table_rows = []

    for line in lines:
        if line.startswith("```"):
            if in_pre:
                body_html.append("</pre>")
                in_pre = False
            else:
                body_html.append("<pre>")
                in_pre = True
            continue

        if in_pre:
            body_html.append(html_lib.escape(line))
            continue

        if line.startswith("|") and line.endswith("|"):
            # Table row
            if "---" in line:
                continue  # Divider
            cols = [c.strip() for c in line.strip("|").split("|")]
            if not in_table:
                in_table = True
                table_rows.append("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody>")
            else:
                table_rows.append("<tr>" + "".join(f"<td>{c}</td>" for c in cols) + "</tr>")
            continue
        else:
            if in_table:
                table_rows.append("</tbody></table>")
                body_html.append("\n".join(table_rows))
                table_rows = []
                in_table = False

        if line.startswith("# "):
            body_html.append(f'<h1 class="doc-title">{line[2:]}</h1>')
        elif line.startswith("## "):
            body_html.append(f'<h2 class="doc-section">{line[3:]}</h2>')
        elif line.startswith("### "):
            body_html.append(f'<h3 class="doc-sub">{line[4:]}</h3>')
        elif line.startswith("- "):
            body_html.append(f'<li>{line[2:]}</li>')
        elif line.strip() == "---":
            body_html.append('<hr class="divider">')
        elif line.strip():
            body_html.append(f'<p>{line}</p>')

    if in_table:
        table_rows.append("</tbody></table>")
        body_html.append("\n".join(table_rows))

    content = "\n".join(body_html)

    # Replace inline formatting
    import re
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>QueryLang Review 3 Final Project Report</title>
<style>
  @page {{
    size: A4;
    margin: 1.8cm 2cm 2cm 2cm;
    @bottom-right {{
      content: counter(page);
    }}
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}
  h1.doc-title {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 24pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
    margin-bottom: 12px;
    border-bottom: 3px solid #2563eb;
    padding-bottom: 8px;
  }}
  h2.doc-section {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 15pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 24px;
    margin-bottom: 8px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
    page-break-after: avoid;
  }}
  h3.doc-sub {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 12.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 16px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  p {{
    margin-bottom: 10px;
    text-align: justify;
  }}
  li {{
    margin-bottom: 4px;
    margin-left: 20px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
    margin: 14px 0;
    page-break-inside: avoid;
  }}
  th {{
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 7px 9px;
    border: 1px solid #cbd5e1;
  }}
  td {{
    padding: 6px 9px;
    border: 1px solid #e2e8f0;
    color: #334155;
  }}
  tr:nth-child(even) td {{
    background: #f8fafc;
  }}
  pre {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3px solid #2563eb;
    color: #0f172a;
    padding: 10px 14px;
    font-family: "Consolas", monospace;
    font-size: 9pt;
    line-height: 1.35;
    margin: 12px 0;
    white-space: pre-wrap;
    page-break-inside: avoid;
  }}
  code {{
    font-family: "Consolas", monospace;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 9.5pt;
  }}
  pre code {{
    background: transparent;
    padding: 0;
  }}
  hr.divider {{
    border: 0;
    border-top: 1px solid #cbd5e1;
    margin: 20px 0;
  }}
</style>
</head>
<body>
{content}
</body>
</html>
"""
    return html


def convert_html_to_pdf(html_path: str, pdf_path: str):
    """Invokes Microsoft Edge headless to render pixel-perfect PDF."""
    cmd = [
        EDGE_EXE,
        "--headless=new",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        html_path
    ]
    print(f"Rendering PDF: {os.path.basename(pdf_path)}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering PDF {pdf_path}: {res.stderr}")
    else:
        print(f"Successfully generated: {pdf_path}")


def main():
    print("=" * 80)
    print("      BUILDING QUERYLANG REVIEW 3 PDF DELIVERABLES")
    print("=" * 80)

    scratch_dir = os.path.join(PROJECT_DIR, ".pdf_scratch")
    os.makedirs(scratch_dir, exist_ok=True)

    # 1. Generate Presentation HTML & PDF
    pres_html = generate_presentation_html()
    pres_html_path = os.path.join(scratch_dir, "presentation.html")
    with open(pres_html_path, "w", encoding="utf-8") as f:
        f.write(pres_html)

    desktop_pres_pdf = os.path.join(DESKTOP_DIR, "QueryLang_Review3_compiler.pdf")
    convert_html_to_pdf(pres_html_path, desktop_pres_pdf)

    # Mirror to QueryLang folder
    local_pres_pdf = os.path.join(PROJECT_DIR, "QueryLang_Review3_compiler.pdf")
    shutil.copy2(desktop_pres_pdf, local_pres_pdf)

    # 2. Generate Report HTML & PDF
    report_html = generate_report_html()
    report_html_path = os.path.join(scratch_dir, "report.html")
    with open(report_html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    desktop_report_pdf = os.path.join(DESKTOP_DIR, "QueryLang_Review3_Report.pdf")
    convert_html_to_pdf(report_html_path, desktop_report_pdf)

    # Mirror to QueryLang folder
    local_report_pdf = os.path.join(PROJECT_DIR, "QueryLang_Review3_Report.pdf")
    shutil.copy2(desktop_report_pdf, local_report_pdf)

    print("\n" + "=" * 80)
    print("ALL REVIEW 3 DELIVERABLES COMPILED SUCCESSFULLY:")
    print(f"  [x] Presentation PDF: {desktop_pres_pdf}")
    print(f"  [x] Academic Report PDF: {desktop_report_pdf}")
    print(f"  [x] Mirrored in QueryLang directory")
    print("=" * 80)


if __name__ == "__main__":
    main()
