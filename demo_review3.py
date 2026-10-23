"""
QueryLang Review 3 Final Interactive Demonstration Script
Executes the six canonical live demonstrations for Review 3 / Final Evaluation.
Demonstrates:
  Demo 1: Full Compiler Pipeline with Rule-Based Optimization (Constant Folding & Simplification)
  Demo 2: Multi-Table Relational INNER JOIN with Qualified Column References
  Demo 3: Filter Pushdown Past Relational Join (Cardinality Reduction)
  Demo 4: Aggregations (COUNT, AVG, MAX, MIN, SUM)
  Demo 5: Performance Benchmarks (Unoptimized vs. Optimized on 100, 1k, 10k rows)
  Demo 6: Comprehensive Diagnostics (Lexical, Syntax, Semantic, Type-Checking) & DOT Visualizer
"""

import sys
import os
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from querylang.pipeline import CompilerPipeline
from querylang.errors import QueryLangError
from querylang.schema.catalog import DEFAULT_CATALOG
from querylang.visualization.visualizer import DOTExporter, export_dot
from querylang.benchmarks.benchmark import run_benchmark_scale, format_benchmark_report


def separator(title: str = ""):
    print("\n" + "=" * 82)
    if title:
        print(f" >>> {title.upper()} <<<")
        print("=" * 82)


def run_review3_demo():
    pipeline = CompilerPipeline()

    print("\n" + "#" * 82)
    print("      QUERYLANG: A COMPILER-STYLE QUERY PROCESSING ENGINE")
    print("               PHASE 3 / FINAL PROJECT REVIEW DEMONSTRATION")
    print("               Student: Aman Katakwar | Reg: 24BCE0160")
    print("               Course: BCSE307P Compiler Design | Guide: Prof. Ranjithkumar S")
    print("#" * 82)

    # -------------------------------------------------------------
    # DEMO 1: Pipeline & Rule-Based Query Optimization
    # -------------------------------------------------------------
    separator("Demo 1: Full Compiler Pipeline & Optimization (Constant Folding & Simplification)")
    q1 = "SELECT name, branch, cgpa FROM students WHERE age >= (18 + 2) AND (1 = 1) ORDER BY cgpa DESC LIMIT 3;"
    print(f"Query: {q1}\n")
    insp1 = pipeline.inspect_query(q1)

    print("--- [STAGE 1] TOKENS (LEXICAL ANALYSIS) ---")
    for t in insp1.tokens:
        print(f"  {t.format_row()}")

    print("\n--- [STAGE 2] AST (SYNTAX ANALYSIS) ---")
    print(insp1.ast_tree_repr)

    print("--- [STAGE 3] SEMANTIC VALIDATION & SYMBOL BINDING ---")
    tbl = insp1.validated_query.table_symbol
    cols = [f"{getattr(c, 'display_name', getattr(c, 'name', str(c)))}:{getattr(c, 'data_type', 'ANY')}" for c in insp1.validated_query.projected_columns]
    print(f"  Bound Table: {tbl.name}")
    print(f"  Bound Projected Columns: [{', '.join(cols)}]")
    print("  Semantic Status: VALIDATED")

    print("\n--- [STAGE 4 & 5] OPTIMIZER COMPARISON REPORT ---")
    print(insp1.optimization_result.format_comparison())

    print("\n--- [STAGE 6] EXECUTED TABULAR RESULT ---")
    print(insp1.result.format_table())

    # -------------------------------------------------------------
    # DEMO 2: Multi-Table Relational INNER JOIN
    # -------------------------------------------------------------
    separator("Demo 2: Multi-Table Relational INNER JOIN with Qualified Columns")
    q2 = """
    SELECT students.name, departments.dept_name, departments.building
    FROM students
    JOIN departments ON students.branch = departments.dept_name
    WHERE students.cgpa >= 8.5;
    """
    print(f"Query:\n{q2.strip()}\n")
    insp2 = pipeline.inspect_query(q2)
    print("--- RELATIONAL JOIN EXECUTION PLAN ---")
    print(insp2.plan_tree_repr)
    print("--- JOIN QUERY RESULT ---")
    print(insp2.result.format_table())

    # -------------------------------------------------------------
    # DEMO 3: Filter Pushdown Past Join
    # -------------------------------------------------------------
    separator("Demo 3: Algebraic Filter Pushdown Optimization")
    q3 = """
    SELECT students.name, departments.dept_name
    FROM students
    JOIN departments ON students.branch = departments.dept_name
    WHERE students.age > 20;
    """
    print(f"Query:\n{q3.strip()}\n")
    insp3 = pipeline.inspect_query(q3)
    print(insp3.optimization_result.format_comparison())

    # -------------------------------------------------------------
    # DEMO 4: Aggregation Functions
    # -------------------------------------------------------------
    separator("Demo 4: Aggregation Operations (COUNT, AVG, MAX, MIN, SUM)")
    q4 = "SELECT COUNT(*), AVG(cgpa), MAX(cgpa), MIN(age), SUM(cgpa) FROM students;"
    print(f"Query: {q4}\n")
    insp4 = pipeline.inspect_query(q4)
    print("--- AGGREGATE EXECUTION PLAN ---")
    print(insp4.plan_tree_repr)
    print("--- AGGREGATE RESULT ---")
    print(insp4.result.format_table())

    # -------------------------------------------------------------
    # DEMO 5: Performance Benchmarking
    # -------------------------------------------------------------
    separator("Demo 5: Performance Benchmarks (Unoptimized vs. Optimized on 100, 1k, 10k rows)")
    bench_q = """
    SELECT students.name, departments.dept_name
    FROM students
    JOIN departments ON students.branch = departments.dept_name
    WHERE students.age > (18 + 2) AND students.cgpa > 8.0;
    """
    bench_results = run_benchmark_scale(bench_q, scales=[100, 1000, 10000], iterations=3)
    print(format_benchmark_report(bench_q, bench_results))

    # -------------------------------------------------------------
    # DEMO 6: Diagnostics and Visualizer Export
    # -------------------------------------------------------------
    separator("Demo 6: Comprehensive Diagnostics & Graphviz DOT Export")

    # 6A: Lexical Error
    q6a = "SELECT name @ students;"
    print(f"Case 6A - Lexical Error:\nQuery: {q6a}")
    try:
        pipeline.execute_query(q6a)
    except QueryLangError as err:
        print(err.format_diagnostic(q6a))

    print("\n" + "-" * 40 + "\n")

    # 6B: Syntax Error
    q6b = "SELECT FROM students;"
    print(f"Case 6B - Syntax Error:\nQuery: {q6b}")
    try:
        pipeline.execute_query(q6b)
    except QueryLangError as err:
        print(err.format_diagnostic(q6b))

    print("\n" + "-" * 40 + "\n")

    # 6C: Semantic Error
    q6c = "SELECT salary FROM students;"
    print(f"Case 6C - Semantic Error (Unknown Column):\nQuery: {q6c}")
    try:
        pipeline.execute_query(q6c)
    except QueryLangError as err:
        print(err.format_diagnostic(q6c))

    print("\n" + "-" * 40 + "\n")

    # 6D: Type Check Error
    q6d = "SELECT name FROM students WHERE name > 50;"
    print(f"Case 6D - Semantic Error (Type Mismatch):\nQuery: {q6d}")
    try:
        pipeline.execute_query(q6d)
    except QueryLangError as err:
        print(err.format_diagnostic(q6d))

    print("\n" + "-" * 40 + "\n")

    # 6E: Graphviz Export
    print("Case 6E - Graphviz DOT Export:")
    demo_dot_query = "SELECT name, branch FROM students WHERE age >= 20;"
    insp_dot = pipeline.inspect_query(demo_dot_query)
    dot_ast_path = os.path.join(os.path.dirname(__file__), "querylang_ast.dot")
    dot_plan_path = os.path.join(os.path.dirname(__file__), "querylang_plan.dot")
    export_dot(insp_dot.dot_ast, dot_ast_path)
    export_dot(insp_dot.dot_plan, dot_plan_path)
    print(f"  [x] Exported AST Graphviz DOT:  {dot_ast_path}")
    print(f"  [x] Exported Plan Graphviz DOT: {dot_plan_path}")

    separator("DEMONSTRATION COMPLETE - ALL 6 DEMOS EXECUTED SUCCESSFULLY")


if __name__ == '__main__':
    run_review3_demo()
