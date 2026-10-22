"""
Script to build high-quality downloadable presentation slides PDF and progress report PDF
for QueryLang Review 2 using Microsoft Edge headless PDF rendering.
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
<title>Review 2 - QueryLang Presentation</title>
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
    padding: 0.8in 1.1in 0.7in 1.1in;
    background: #ffffff;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  /* Slide Header */
  .slide-header {
    margin-bottom: 0.35in;
  }
  .slide-title {
    font-size: 34pt;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.5px;
  }
  .slide-subtitle {
    font-size: 16pt;
    color: #64748b;
    margin-top: 4px;
    font-weight: 500;
  }
  /* Slide Footer */
  .slide-footer {
    position: absolute;
    bottom: 0.4in;
    left: 1.1in;
    right: 1.1in;
    border-top: 1.5px solid #cbd5e1;
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
    font-size: 12pt;
    color: #64748b;
  }
  .slide-number {
    font-weight: 600;
    color: #334155;
  }
  /* Content Elements */
  .content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  .columns-2 {
    display: flex;
    gap: 0.6in;
    flex: 1;
  }
  .col {
    flex: 1;
  }
  .card {
    background: #f8fafc;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.25in 0.35in;
    margin-bottom: 0.2in;
  }
  .card-title {
    font-size: 18pt;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 10px;
  }
  p, li {
    font-size: 14.5pt;
    line-height: 1.5;
    color: #334155;
  }
  ul {
    margin-left: 24px;
    margin-top: 8px;
  }
  li {
    margin-bottom: 8px;
  }
  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5pt;
    margin-top: 10px;
  }
  th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 11px 14px;
    border-bottom: 2px solid #cbd5e1;
  }
  td {
    padding: 10px 14px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
  }
  tr:nth-child(even) td {
    background: #f8fafc;
  }
  /* Badges */
  .badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11pt;
    font-weight: 700;
  }
  .badge-pass { background: #dcfce7; color: #15803d; }
  .badge-blue { background: #dbeafe; color: #1d4ed8; }
  .badge-purple { background: #f3e8ff; color: #7e22ce; }
  /* Code blocks */
  pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 14px 18px;
    border-radius: 8px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12.5pt;
    line-height: 1.4;
    overflow: hidden;
  }
  /* Pipeline blocks */
  .pipeline-flow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 25px 0;
  }
  .pipe-node {
    background: #ffffff;
    border: 2px solid #0284c7;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: center;
    font-weight: 700;
    font-size: 13pt;
    color: #0369a1;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    min-width: 1.6in;
  }
  .pipe-arrow {
    font-size: 20pt;
    font-weight: bold;
    color: #94a3b8;
  }

  /* Title Slide Specifics */
  .title-slide {
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 1.2in 1.5in;
  }
  .title-top-badge {
    font-size: 22pt;
    font-weight: 800;
    letter-spacing: 2px;
    color: #0f172a;
    margin-bottom: 25px;
    text-transform: uppercase;
  }
  .title-main {
    font-size: 44pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 20px;
    line-height: 1.15;
  }
  .title-project-sub {
    font-size: 22pt;
    color: #475569;
    font-weight: 500;
    margin-bottom: 45px;
  }
  .title-meta-box {
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 12px;
    padding: 25px 40px;
    display: inline-block;
    text-align: left;
    font-size: 16pt;
    line-height: 1.7;
    color: #1e293b;
    min-width: 6.5in;
  }
  .title-meta-box strong {
    color: #0f172a;
    display: inline-block;
    width: 2.1in;
  }
  .title-footer-note {
    margin-top: 35px;
    font-size: 14pt;
    color: #64748b;
  }
</style>
</head>
<body>

<!-- SLIDE 1: Title Slide -->
<div class="slide title-slide">
  <div class="title-top-badge">REVIEW – 2</div>
  <div class="title-main">QueryLang: A Compiler-Style Query Processing Engine</div>
  <div class="title-project-sub">Compiler Design Laboratory Project (BCSE307P)</div>
  <div class="title-meta-box">
    <div><strong>Name:</strong> Aman Katakwar</div>
    <div><strong>Reg. No.:</strong> 24BCE0160</div>
    <div><strong>Course Code:</strong> BCSE307P</div>
    <div><strong>Submitted to:</strong> Prof. Ranjithkumar S</div>
    <div><strong>Milestone:</strong> Review 2 — Core Implementation & Functional Prototype</div>
  </div>
  <div class="title-footer-note">School of Computer Science and Engineering | Academic Year 2026–27</div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">1</span>
  </div>
</div>

<!-- SLIDE 2: Evolution from Review 1 to Review 2 -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">1. Review 1 to Review 2 Transition</div>
    <div class="slide-subtitle">Progression from design specifications to a fully functioning compiler pipeline</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card" style="border-left: 5px solid #94a3b8;">
          <div class="card-title">Review 1 Deliverables (Phase 1: Design)</div>
          <ul>
            <li>Problem definition, scope, and domain constraints established.</li>
            <li>Formal Context-Free Grammar (CFG) in EBNF specified.</li>
            <li>7-stage compiler architecture planned.</li>
            <li>Working Lexer prototype with tokenization and character diagnostics.</li>
            <li>Subsequent stages explicitly reserved for Phase 2.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card" style="border-left: 5px solid #0284c7;">
          <div class="card-title">Review 2 Deliverables (Phase 2: Implementation)</div>
          <ul>
            <li><strong>Complete Lexer:</strong> Token recognition with precise line/col coordinates.</li>
            <li><strong>Recursive-Descent Parser:</strong> LL(1) predictive grammar analysis.</li>
            <li><strong>Abstract Syntax Tree (AST):</strong> Object-oriented tree nodes & visualizer.</li>
            <li><strong>Symbol Table / Catalog:</strong> Scope management & type declarations.</li>
            <li><strong>Semantic Analyzer:</strong> Name resolution and static type checking.</li>
            <li><strong>Relational Query Planner:</strong> Intermediate Code (IR) generation.</li>
            <li><strong>Execution Engine:</strong> In-memory relational interpretation.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">2</span>
  </div>
</div>

<!-- SLIDE 3: Review 2 Rubric Alignment -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">2. Review 2 Rubric Alignment (25 Marks)</div>
    <div class="slide-subtitle">Strict compliance with the Compiler Design Laboratory Instruction Manual criteria</div>
  </div>
  <div class="content-area">
    <table>
      <thead>
        <tr>
          <th style="width: 28%;">Evaluation Criteria</th>
          <th style="width: 12%;">Marks</th>
          <th style="width: 60%;">QueryLang Implementation & Evidence</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Implementation Progress</strong></td>
          <td><strong>7</strong></td>
          <td>100% of planned Phase 2 modules completed: Lexer &rarr; Parser &rarr; AST &rarr; Symbol Table &rarr; Semantic Analyzer &rarr; Query Planner &rarr; Execution Engine. Zero mock stages.</td>
        </tr>
        <tr>
          <td><strong>Technical Correctness</strong></td>
          <td><strong>5</strong></td>
          <td>Deterministic token scanning, accurate LL(1) recursive-descent parsing, correct AST hierarchy, exact semantic validation, relational operator execution.</td>
        </tr>
        <tr>
          <td><strong>Compiler Concept Application</strong></td>
          <td><strong>4</strong></td>
          <td>Direct application of regular expressions, CFGs, LL(1) predictive parsing, AST construction, symbol tables, static type inference, and intermediate code representation.</td>
        </tr>
        <tr>
          <td><strong>Code Quality</strong></td>
          <td><strong>3</strong></td>
          <td>Clean modular architecture across 8 sub-packages, comprehensive docstrings, meaningful variable/function naming, pure Python 3 standard library (zero external dependencies).</td>
        </tr>
        <tr>
          <td><strong>Testing</strong></td>
          <td><strong>3</strong></td>
          <td>Formal 16-test verification matrix + 20 PyUnit test cases covering positive, compound, error, and boundary conditions (100% pass rate in 0.004s).</td>
        </tr>
        <tr>
          <td><strong>Individual Understanding</strong></td>
          <td><strong>3</strong></td>
          <td>In-depth comprehension of parsing algorithms, relational algebra translation, symbol table scope management, and runtime query interpretation.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">3</span>
  </div>
</div>

<!-- SLIDE 4: Proposed System Architecture -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">3. Core Implementation Architecture & Data Flow</div>
    <div class="slide-subtitle">Modular, inspectable pipeline transforming declarative queries into executed results</div>
  </div>
  <div class="content-area">
    <div class="pipeline-flow">
      <div class="pipe-node">Source<br>Query</div>
      <div class="pipe-arrow">&rarr;</div>
      <div class="pipe-node">Lexical<br>Analyzer</div>
      <div class="pipe-arrow">&rarr;</div>
      <div class="pipe-node">Recursive<br>Parser</div>
      <div class="pipe-arrow">&rarr;</div>
      <div class="pipe-node">Abstract<br>Syntax Tree</div>
      <div class="pipe-arrow">&rarr;</div>
      <div class="pipe-node">Semantic<br>Analyzer</div>
      <div class="pipe-arrow">&rarr;</div>
      <div class="pipe-node">Query<br>Planner (IR)</div>
      <div class="pipe-arrow">&rarr;</div>
      <div class="pipe-node">Execution<br>Engine</div>
    </div>
    <div class="card" style="margin-top: 15px;">
      <div class="card-title">Inter-Module Contracts and Data Representation</div>
      <p style="margin-bottom: 8px;"><strong>1. Tokens:</strong> Token stream with token type, evaluated literal value, line, and column coordinates.</p>
      <p style="margin-bottom: 8px;"><strong>2. AST:</strong> Hierarchical composite tree representing projections, table targets, and binary condition nodes.</p>
      <p style="margin-bottom: 8px;"><strong>3. Symbol Table:</strong> Schema Catalog validating table identifiers, attribute availability, and types.</p>
      <p style="margin-bottom: 8px;"><strong>4. Logical Plan (IR):</strong> Tree of relational algebra operators: SCAN &rarr; FILTER &rarr; PROJECT &rarr; SORT &rarr; LIMIT.</p>
      <p><strong>5. Engine:</strong> Tree-walking runtime interpreter executing plan against in-memory records to produce formatted ASCII tables.</p>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">4</span>
  </div>
</div>

<!-- SLIDE 5: Compiler Design Concepts Used -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">4. Compiler Design Concepts Applied in Phase 2</div>
    <div class="slide-subtitle">Direct theoretical grounding in core language-processing fundamentals</div>
  </div>
  <div class="content-area">
    <table>
      <thead>
        <tr>
          <th style="width: 25%;">Compiler Concept</th>
          <th style="width: 35%;">Theoretical Foundation</th>
          <th style="width: 40%;">QueryLang Implementation Module</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Lexical Analysis</strong></td>
          <td>Regular expressions, DFA state scanning, token classification</td>
          <td><code>querylang/lexer/lexer.py</code></td>
        </tr>
        <tr>
          <td><strong>Syntax Analysis</strong></td>
          <td>Context-Free Grammar (CFG), LL(1) predictive parsing</td>
          <td><code>querylang/parser/parser.py</code></td>
        </tr>
        <tr>
          <td><strong>Abstract Syntax Tree</strong></td>
          <td>Hierarchical syntax tree representation and traversal</td>
          <td><code>querylang/ast/nodes.py</code></td>
        </tr>
        <tr>
          <td><strong>Symbol Table</strong></td>
          <td>Scope resolution, identifier binding, attribute data types</td>
          <td><code>querylang/schema/catalog.py</code></td>
        </tr>
        <tr>
          <td><strong>Semantic Analysis</strong></td>
          <td>Static semantic validation, type inference, type checking</td>
          <td><code>querylang/semantic/analyzer.py</code></td>
        </tr>
        <tr>
          <td><strong>Intermediate Code (IR)</strong></td>
          <td>Relational algebra operator tree (&sigma;, &pi;, &tau;)</td>
          <td><code>querylang/planner/planner.py</code></td>
        </tr>
        <tr>
          <td><strong>Runtime Execution</strong></td>
          <td>Tree-walking evaluation / interpreter on relation records</td>
          <td><code>querylang/execution/engine.py</code></td>
        </tr>
        <tr>
          <td><strong>Diagnostic System</strong></td>
          <td>Contextual error reporting with line/col caret (<code>^</code>) pointers</td>
          <td><code>querylang/errors/errors.py</code></td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">5</span>
  </div>
</div>

<!-- SLIDE 6: Parser Implementation & Grammar -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">5. Recursive-Descent Parser & Formal Grammar</div>
    <div class="slide-subtitle">Top-down predictive parsing implementing stratified operator precedence</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">QueryLang EBNF Grammar</div>
          <pre>
query         ::= SELECT column_list 
                  FROM table_name 
                  [ where_clause ] 
                  [ order_clause ] 
                  [ limit_clause ] ";"
column_list   ::= "*" | col ("," col)*
where_clause  ::= WHERE condition
condition     ::= or_expr
or_expr       ::= and_expr (OR and_expr)*
and_expr      ::= comparison (AND comparison)*
comparison    ::= primary [ comp_op primary ]
primary       ::= col | literal | "(" cond ")"</pre>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Algorithmic Highlights</div>
          <ul>
            <li><strong>Elimination of Ambiguity:</strong> Stratified grammar productions enforce strict operator precedence: <code>OR &lt; AND &lt; COMPARISONS &lt; PARENTHESES</code>.</li>
            <li><strong>Predictive LL(1) Lookahead:</strong> Employs <code>current_token</code> and <code>peek()</code> to deterministically choose production alternatives without backtracking.</li>
            <li><strong>Syntactic Error Recovery:</strong> Mismatched tokens raise explicit <code>SyntaxError</code> reporting exact line, column, expected symbol, and offending token.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">6</span>
  </div>
</div>

<!-- SLIDE 7: Abstract Syntax Tree (AST) Architecture -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">6. Abstract Syntax Tree (AST) Architecture</div>
    <div class="slide-subtitle">Strongly typed object hierarchy representing synthesized query structures</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">AST Node Classes (<code>nodes.py</code>)</div>
          <ul>
            <li><code>SelectQueryNode</code>: Root node encapsulating projection list, table target, condition, sort, and limit.</li>
            <li><code>ColumnNode</code>: Represents attribute references (e.g. <code>name</code>, <code>cgpa</code>).</li>
            <li><code>TableNode</code>: Represents source relation identifiers (e.g. <code>students</code>).</li>
            <li><code>LiteralNode</code>: Encapsulates constants and intrinsic types (<code>INTEGER</code>, <code>FLOAT</code>, <code>STRING</code>, <code>BOOLEAN</code>).</li>
            <li><code>BinaryOpNode</code>: Encapsulates binary operators (<code>AND</code>, <code>OR</code>, <code>&gt;=</code>, <code>=</code>, etc.).</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Generated Visual Tree</div>
          <pre>
SelectQueryNode
|-- Projected Columns: [name, cgpa]
|-- Source Table: students
|-- WHERE Condition:
    \\-- BinaryOpNode(AND)
        |-- BinaryOpNode(>=)
        |   |-- ColumnNode(cgpa)
        |   \\-- LiteralNode(8.5 : FLOAT)
        \\-- BinaryOpNode(>)
            |-- ColumnNode(age)
            \\-- LiteralNode(20 : INTEGER)</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">7</span>
  </div>
</div>

<!-- SLIDE 8: Symbol Table Management -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">7. Symbol Table Management (Schema Catalog)</div>
    <div class="slide-subtitle">Centralized repository for relational schema, attribute scopes, and data types</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Symbol Table Architecture</div>
          <ul>
            <li><strong>Relational Catalog:</strong> In QueryLang, the traditional compiler symbol table is embodied by the <code>SchemaCatalog</code>.</li>
            <li><strong>Table Scope:</strong> <code>TableSymbol</code> manages table identifiers and child column definitions.</li>
            <li><strong>Attribute Symbols:</strong> <code>ColumnSymbol</code> tracks column identifiers, data types, and semantic constraints.</li>
            <li><strong>Lookup Methods:</strong> Provides O(1) scope lookups: <code>has_table()</code>, <code>get_table()</code>, <code>has_column()</code>.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Default Preloaded Schema (<code>students</code>)</div>
          <table>
            <thead>
              <tr><th>Column Identifier</th><th>Declared Type</th><th>Semantic Role</th></tr>
            </thead>
            <tbody>
              <tr><td><code>id</code></td><td>INTEGER</td><td>Primary key</td></tr>
              <tr><td><code>name</code></td><td>STRING</td><td>Student full name</td></tr>
              <tr><td><code>age</code></td><td>INTEGER</td><td>Age in years</td></tr>
              <tr><td><code>branch</code></td><td>STRING</td><td>Academic department</td></tr>
              <tr><td><code>cgpa</code></td><td>FLOAT</td><td>Cumulative GPA</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">8</span>
  </div>
</div>

<!-- SLIDE 9: Semantic Analysis & Static Type Checking -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">8. Semantic Analysis & Type Diagnostics</div>
    <div class="slide-subtitle">Enforcing semantic correctness beyond grammatical validity</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Semantic Validation Steps</div>
          <ul>
            <li><strong>Table Scope Check:</strong> Ensures <code>FROM</code> relation exists in catalog.</li>
            <li><strong>Attribute Scope Check:</strong> Ensures projected attributes and condition columns exist on the referenced relation.</li>
            <li><strong>Static Type Inference:</strong> Traverses condition expression subtrees; resolves column types from symbol table and validates operator compatibility.</li>
            <li><strong>Type Compatibility:</strong> Allows numeric comparisons between <code>INTEGER</code> and <code>FLOAT</code>; disallows illegal operations like <code>STRING &gt; INTEGER</code>.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Context-Aware Error Diagnostics</div>
          <pre>
[SEMANTIC ERROR] at Line 1, Column 8: 
Column 'salary' does not exist in table 'students'.
  --> SELECT salary FROM students;
             ^
  HINT: Available columns in 'students': 
        id, name, age, branch, cgpa

------------------------------------------------
[SEMANTIC ERROR] at Line 1, Column 38: 
Operator '>' cannot be applied to STRING and INTEGER.
  --> SELECT name FROM students WHERE name > 50;
                                           ^</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">9</span>
  </div>
</div>

<!-- SLIDE 10: Intermediate Representation & Query Plan -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">9. Relational Algebra Intermediate Representation (IR)</div>
    <div class="slide-subtitle">Translating decorated AST into a decoupled logical query execution plan</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Relational Operators (<code>planner/plan.py</code>)</div>
          <ul>
            <li><code>ScanNode</code>: Base relation access operator.</li>
            <li><code>FilterNode</code>: Selection operator (&sigma;) filtering tuples by predicate.</li>
            <li><code>ProjectNode</code>: Projection operator (&pi;) discarding non-requested attributes.</li>
            <li><code>SortNode</code>: Ordering operator (&tau;) sorting dataset tuples.</li>
            <li><code>LimitNode</code>: Cardinality operator truncating output rows.</li>
            <li><strong>Decoupling Benefit:</strong> Isolates query parsing from evaluation, enabling algebraic optimizations in Phase 3.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Generated Logical Plan Tree (IR)</div>
          <pre>
\\-- PROJECT [name, cgpa]
    \\-- FILTER [cgpa >= 8.5 AND age > 20]
        \\-- SCAN [students]

Formal Relational Algebra Expression:
&pi;_{name, cgpa} ( &sigma;_{cgpa &ge; 8.5 &and; age &gt; 20} ( SCAN(students) ) )</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">10</span>
  </div>
</div>

<!-- SLIDE 11: In-Memory Execution Engine -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">10. In-Memory Execution Engine & Results</div>
    <div class="slide-subtitle">Runtime interpreter evaluating the logical plan over in-memory datasets</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Engine Execution Architecture</div>
          <ul>
            <li><strong>Tree-Walking Interpreter:</strong> Recursively executes logical plan operators over in-memory relational dictionaries.</li>
            <li><strong>Predicate Evaluation:</strong> Expression tree evaluator supporting comparison operators and boolean short-circuit logic (<code>AND</code>, <code>OR</code>).</li>
            <li><strong>Performance Telemetry:</strong> Automatically measures rows scanned, rows filtered, and rows returned.</li>
            <li><strong>ASCII Table Formatter:</strong> Renders dynamically sized tabular result sets.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Canonical Query Execution Result</div>
          <pre>
Query: 
SELECT name, cgpa FROM students 
WHERE cgpa >= 8.5 AND age > 20;

+--------+--------+
| NAME   | CGPA   |
+--------+--------+
| Asha   | 8.7    |
| Rahul  | 9.1    |
| Pooja  | 8.9    |
| Ananya | 9.4    |
+--------+--------+
4 row(s) in set (Scanned: 7, Filtered: 4)</pre>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">11</span>
  </div>
</div>

<!-- SLIDE 12: Comprehensive Testing Matrix -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">11. Comprehensive Testing Matrix & Verification</div>
    <div class="slide-subtitle">Automated verification matrix and PyUnit test harness results (100% pass rate)</div>
  </div>
  <div class="content-area">
    <table>
      <thead>
        <tr>
          <th style="width: 10%;">Test ID</th>
          <th style="width: 25%;">Category</th>
          <th style="width: 35%;">Input Query / Condition</th>
          <th style="width: 18%;">Expected Output</th>
          <th style="width: 12%;">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>T-01</code></td>
          <td>Basic SELECT</td>
          <td><code>SELECT name FROM students;</code></td>
          <td>7 rows returned</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
        <tr>
          <td><code>T-03</code></td>
          <td>WHERE Filter</td>
          <td><code>SELECT name FROM students WHERE age &gt; 20;</code></td>
          <td>4 rows filtered</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
        <tr>
          <td><code>T-04</code></td>
          <td>Logical AND</td>
          <td><code>SELECT name, cgpa FROM students WHERE cgpa &gt;= 8.5 AND age &gt; 20;</code></td>
          <td>4 rows filtered</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
        <tr>
          <td><code>T-07</code></td>
          <td>ORDER BY</td>
          <td><code>SELECT name, cgpa FROM students ORDER BY cgpa;</code></td>
          <td>Sorted ascending</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
        <tr>
          <td><code>T-09</code></td>
          <td>Lexical Error</td>
          <td><code>SELECT name @ students;</code></td>
          <td>LexicalError raised</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
        <tr>
          <td><code>T-10</code></td>
          <td>Syntax Error</td>
          <td><code>SELECT FROM students;</code></td>
          <td>SyntaxError raised</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
        <tr>
          <td><code>T-13</code></td>
          <td>Semantic Error</td>
          <td><code>SELECT salary FROM students;</code></td>
          <td>SemanticError raised</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
        <tr>
          <td><code>T-14</code></td>
          <td>Type Mismatch</td>
          <td><code>SELECT name FROM students WHERE name &gt; 50;</code></td>
          <td>SemanticError raised</td>
          <td><span class="badge badge-pass">PASS</span></td>
        </tr>
      </tbody>
    </table>
    <div style="margin-top: 15px; font-size: 13.5pt; color: #15803d; font-weight: bold;">
      &check; Total Tests: 16 Formal Matrix Tests + 20 PyUnit Test Cases | Passed: 100% | Execution Time: 0.004s
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">12</span>
  </div>
</div>

<!-- SLIDE 13: Live Demonstration Scenarios -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">12. Live Demonstration Scenarios (Demos 1 to 5)</div>
    <div class="slide-subtitle">Pre-configured operational scenarios ready for interactive evaluation</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card">
          <div class="card-title">Demos 1 to 4: Functional Scenarios</div>
          <p style="margin-bottom: 8px;"><strong>Demo 1: Basic Projection</strong><br>
          <code>SELECT name FROM students;</code> &rarr; Validates projection without filter.</p>
          <p style="margin-bottom: 8px;"><strong>Demo 2: Relational Filtering</strong><br>
          <code>SELECT name, age, cgpa FROM students WHERE age &gt; 20;</code> &rarr; Evaluates condition operator.</p>
          <p style="margin-bottom: 8px;"><strong>Demo 3: Semantic Diagnostics</strong><br>
          <code>SELECT salary FROM students;</code> &rarr; Catches missing attribute with column hints.</p>
          <p><strong>Demo 4: Syntactic Diagnostics</strong><br>
          <code>SELECT FROM students;</code> &rarr; Catches missing projection column.</p>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-title">Demo 5: Deep-Dive Pipeline Inspection</div>
          <p style="margin-bottom: 10px;">Canonical Query: <code>SELECT name, cgpa FROM students WHERE cgpa &gt;= 8.5 AND age &gt; 20;</code></p>
          <ul style="font-size: 13.5pt;">
            <li><strong>Stage 1 (Lexer):</strong> Full token stream with line and col markers.</li>
            <li><strong>Stage 2 (Parser):</strong> Hierarchical AST visual tree output.</li>
            <li><strong>Stage 3 (Semantic):</strong> Symbol binding & type checks confirmed.</li>
            <li><strong>Stage 4 (Planner):</strong> Relational algebra IR execution tree.</li>
            <li><strong>Stage 5 (Engine):</strong> Formatted result set with execution metrics.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">13</span>
  </div>
</div>

<!-- SLIDE 14: Conclusion & Phase 3 Roadmap -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-title">13. Conclusion & Phase 3 Roadmap</div>
    <div class="slide-subtitle">Review 2 accomplishments and preparation for final submission</div>
  </div>
  <div class="content-area">
    <div class="columns-2">
      <div class="col">
        <div class="card" style="border-left: 5px solid #16a34a;">
          <div class="card-title">Review 2 Accomplishments</div>
          <ul>
            <li>Transitioned from an isolated lexer prototype to a complete, operational compiler pipeline.</li>
            <li>Demonstrated concrete practical implementations of Lexer, Parser, AST, Symbol Table, Semantic Analyzer, IR Planner, and Execution Engine.</li>
            <li>Constructed an automated verification test suite and multi-case demonstration runner.</li>
          </ul>
        </div>
      </div>
      <div class="col">
        <div class="card" style="border-left: 5px solid #d97706;">
          <div class="card-title">Phase 3 Planned Deliverables</div>
          <ul>
            <li><strong>Query Optimizer:</strong> Rule-based algebraic rewrites (predicate pushdown, constant folding, tautology elimination).</li>
            <li><strong>Language Extensions:</strong> Multi-table relational JOINs and aggregate functions (<code>COUNT</code>, <code>AVG</code>, <code>SUM</code>).</li>
            <li><strong>Interactive UI:</strong> GUI / Web visualizer for query pipeline inspection.</li>
            <li><strong>Performance Benchmarks:</strong> Comparative execution timing across varying dataset scales.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>QueryLang: Review 2 Core Implementation</span>
    <span class="slide-number">14</span>
  </div>
</div>

</body>
</html>"""
    return html


def generate_report_html() -> str:
    # Read the markdown report
    report_md_path = os.path.join(PROJECT_DIR, "REVIEW_2_REPORT.md")
    with open(report_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown basics to clean HTML for printing
    import html as html_lib
    
    # Simple, reliable conversion of headings, codeblocks, tables, lists, and bold text
    lines = md_content.splitlines()
    html_lines = []
    in_code = False
    code_block = []
    in_table = False
    table_rows = []

    for line in lines:
        if line.startswith("```"):
            if in_code:
                in_code = False
                code_text = html_lib.escape("\n".join(code_block))
                html_lines.append(f"<pre><code>{code_text}</code></pre>")
                code_block.clear()
            else:
                in_code = True
            continue

        if in_code:
            code_block.append(line)
            continue

        # Handle tables
        if line.strip().startswith("|") and line.strip().endswith("|"):
            parts = [p.strip() for p in line.strip()[1:-1].split("|")]
            # Check if separator
            if all(set(p).issubset({'-', ':', ' '}) for p in parts if p):
                continue
            table_rows.append(parts)
            in_table = True
            continue
        elif in_table:
            # Flush table
            th = True
            tbl_html = ["<table>"]
            for r in table_rows:
                tbl_html.append("<tr>")
                tag = "th" if th else "td"
                for cell in r:
                    # Simple bold formatting inside cell
                    cell_clean = html_lib.escape(cell).replace("&lt;strong&gt;", "<strong>").replace("&lt;/strong&gt;", "</strong>")
                    cell_clean = cell_clean.replace("&amp;rarr;", "&rarr;").replace("&amp;le;", "&le;").replace("&amp;ge;", "&ge;")
                    cell_clean = cell_clean.replace("**", "<strong>", 1).replace("**", "</strong>", 1) if "**" in cell_clean else cell_clean
                    tbl_html.append(f"<{tag}>{cell_clean}</{tag}>")
                tbl_html.append("</tr>")
                th = False
            tbl_html.append("</table>")
            html_lines.append("\n".join(tbl_html))
            table_rows.clear()
            in_table = False

        stripped = line.strip()
        if not stripped:
            html_lines.append("<br>")
            continue

        if stripped.startswith("# "):
            html_lines.append(f"<h1>{html_lib.escape(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{html_lib.escape(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{html_lib.escape(stripped[4:])}</h3>")
        elif stripped.startswith("#### "):
            html_lines.append(f"<h4>{html_lib.escape(stripped[5:])}</h4>")
        elif stripped.startswith("- "):
            html_lines.append(f"<li>{html_lib.escape(stripped[2:])}</li>")
        elif stripped.startswith("> "):
            html_lines.append(f"<blockquote>{html_lib.escape(stripped[2:])}</blockquote>")
        elif stripped.startswith("---"):
            html_lines.append("<hr>")
        else:
            # Inline formatting
            p_text = html_lib.escape(stripped)
            # handle strong
            while "**" in p_text:
                p_text = p_text.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            # handle code
            while "`" in p_text:
                p_text = p_text.replace("`", "<code>", 1).replace("`", "</code>", 1)
            html_lines.append(f"<p>{p_text}</p>")

    if in_table and table_rows:
        th = True
        tbl_html = ["<table>"]
        for r in table_rows:
            tbl_html.append("<tr>")
            tag = "th" if th else "td"
            for cell in r:
                tbl_html.append(f"<{tag}>{html_lib.escape(cell)}</{tag}>")
            tbl_html.append("</tr>")
            th = False
        tbl_html.append("</table>")
        html_lines.append("\n".join(tbl_html))

    body_content = "\n".join(html_lines)

    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>QueryLang Review 2 Progress Report</title>
<style>
  @page {{
    size: A4;
    margin: 20mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: "Segoe UI", -apple-system, Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.6;
    font-size: 11pt;
    padding: 0 10px;
  }}
  h1 {{
    font-size: 24pt;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 8px;
    margin-top: 24px;
    margin-bottom: 12px;
  }}
  h2 {{
    font-size: 17pt;
    color: #0369a1;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 6px;
    margin-top: 22px;
    margin-bottom: 10px;
  }}
  h3 {{
    font-size: 13pt;
    color: #0f172a;
    margin-top: 16px;
    margin-bottom: 6px;
  }}
  p {{
    margin-bottom: 10px;
    text-align: justify;
  }}
  li {{
    margin-left: 20px;
    margin-bottom: 5px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 10pt;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }}
  th {{
    background: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
  }}
  tr:nth-child(even) td {{
    background: #f8fafc;
  }}
  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: "Consolas", monospace;
    font-size: 9pt;
    line-height: 1.35;
    margin: 12px 0;
    page-break-inside: avoid;
  }}
  code {{
    background: #e2e8f0;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
    font-family: "Consolas", monospace;
    font-size: 9.5pt;
  }}
  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}
  blockquote {{
    border-left: 4px solid #0284c7;
    background: #f0f9ff;
    padding: 10px 15px;
    margin: 12px 0;
    color: #0369a1;
    font-style: italic;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 20px 0;
  }}
</style>
</head>
<body>
{body_content}
</body>
</html>"""
    return report_html


def main():
    print("=" * 80)
    print("Building Review 2 Presentation Slides PDF & Academic Progress Report PDF...")
    print("=" * 80)

    # 1. Presentation Slides PDF
    pres_html = generate_presentation_html()
    temp_pres_html = os.path.join(PROJECT_DIR, "presentation_temp.html")
    with open(temp_pres_html, "w", encoding="utf-8") as f:
        f.write(pres_html)

    pres_pdf_desktop = os.path.join(DESKTOP_DIR, "QueryLang_Review2_compiler.pdf")
    pres_pdf_project = os.path.join(PROJECT_DIR, "QueryLang_Review2_compiler.pdf")

    print(f"1. Rendering Presentation PDF: {pres_pdf_desktop}")
    cmd_pres = [
        EDGE_EXE,
        "--headless=new",
        f"--print-to-pdf={pres_pdf_desktop}",
        "--no-pdf-header-footer",
        temp_pres_html
    ]
    subprocess.run(cmd_pres, check=True)
    shutil.copyfile(pres_pdf_desktop, pres_pdf_project)

    if os.path.exists(temp_pres_html):
        os.remove(temp_pres_html)

    # 2. Formal Academic Report PDF
    report_html = generate_report_html()
    temp_report_html = os.path.join(PROJECT_DIR, "report_temp.html")
    with open(temp_report_html, "w", encoding="utf-8") as f:
        f.write(report_html)

    report_pdf_desktop = os.path.join(DESKTOP_DIR, "QueryLang_Review2_Report.pdf")
    report_pdf_project = os.path.join(PROJECT_DIR, "QueryLang_Review2_Report.pdf")

    print(f"2. Rendering Formal Report PDF: {report_pdf_desktop}")
    cmd_rep = [
        EDGE_EXE,
        "--headless=new",
        f"--print-to-pdf={report_pdf_desktop}",
        temp_report_html
    ]
    subprocess.run(cmd_rep, check=True)
    shutil.copyfile(report_pdf_desktop, report_pdf_project)

    if os.path.exists(temp_report_html):
        os.remove(temp_report_html)

    print("\n" + "=" * 80)
    print("ALL DOWNLOADABLE PDF FORMATS READY ON YOUR DESKTOP & PROJECT FOLDER:")
    print(f"  [Presentation Slides] -> {pres_pdf_desktop}")
    print(f"  [Academic Report]     -> {report_pdf_desktop}")
    print("=" * 80)


if __name__ == '__main__':
    main()
