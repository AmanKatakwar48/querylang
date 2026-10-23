"""
QueryLang Interactive CLI and Compiler Driver (Review 3 Final)
Main entry point for BCSE307P Compiler Design Laboratory - Final Project Review.
Supports interactive query execution, rule-based optimization inspection,
multi-table joins, aggregations, benchmarks, Graphviz DOT export, and test suite verification.
"""

import sys
import os
import argparse
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from querylang.pipeline import CompilerPipeline
from querylang.schema.catalog import DEFAULT_CATALOG
from querylang.errors import QueryLangError
from querylang.visualization.visualizer import DOTExporter, export_dot
from querylang.benchmarks.benchmark import run_benchmark_scale, format_benchmark_report
from demo_review3 import run_review3_demo
from tests.run_all_tests import run_formal_test_suite


BANNER = r"""
================================================================================
   QueryLang: A Compiler-Style Query Processing Engine (Review 3 Final)
   Student: Aman Katakwar (24BCE0160) | Faculty Guide: Prof. Ranjithkumar S
   Course: BCSE307P Compiler Design Laboratory
================================================================================
Interactive Shell Commands:
  \help          - Show this help message
  \schema        - Display Symbol Table (Schema Catalog)
  \inspect <sql> - Run query with 6-stage compiler inspection + optimizer report
  \demo          - Run the comprehensive Review 3 live demonstration suite
  \benchmark     - Run the synthetic dataset scale benchmark (100, 1k, 10k rows)
  \test          - Run the 25-test verification matrix & formal PyUnit suite
  \dot <sql>     - Export Graphviz DOT files (querylang_ast.dot & querylang_plan.dot)
  \quit or \exit - Exit the shell
================================================================================
"""


def inspect_and_display(pipeline: CompilerPipeline, query: str):
    print("\n" + "=" * 82)
    print(f"COMPILER PIPELINE STAGE-BY-STAGE INSPECTION: {query}")
    print("=" * 82)
    try:
        insp = pipeline.inspect_query(query, optimize=True)

        print("\n--- [STAGE 1] TOKENS (LEXICAL ANALYSIS) ---")
        for t in insp.tokens:
            print(f"  {t.format_row()}")

        print("\n--- [STAGE 2] AST (SYNTAX ANALYSIS) ---")
        print(insp.ast_tree_repr)

        print("--- [STAGE 3] SEMANTIC VALIDATION & SYMBOL BINDING ---")
        tbl = insp.validated_query.table_symbol
        cols = [f"{getattr(c, 'display_name', getattr(c, 'name', str(c)))}:{getattr(c, 'data_type', 'ANY')}" for c in insp.validated_query.projected_columns]
        print(f"  Bound Primary Table: {tbl.name}")
        if insp.validated_query.joined_table_symbol:
            print(f"  Bound Joined Table:  {insp.validated_query.joined_table_symbol.name}")
        print(f"  Bound Projected Columns: [{', '.join(cols)}]")
        print("  Semantic Status: VALIDATED")

        print("\n--- [STAGE 4 & 5] OPTIMIZER COMPARISON REPORT ---")
        if insp.optimization_result:
            print(insp.optimization_result.format_comparison())
        else:
            print("--- LOGICAL QUERY PLAN ---")
            print(insp.plan_tree_repr)

        print("\n--- [STAGE 6] EXECUTED TABULAR RESULT ---")
        print(insp.result.format_table())
        print("=" * 82 + "\n")

    except QueryLangError as err:
        print("\n" + err.format_diagnostic(query))
        print("=" * 82 + "\n")


def execute_single_query(pipeline: CompilerPipeline, query: str, inspect: bool = False):
    if inspect:
        inspect_and_display(pipeline, query)
    else:
        try:
            res = pipeline.execute_query(query, optimize=True)
            print()
            print(res.format_table())
            print()
        except QueryLangError as err:
            print()
            print(err.format_diagnostic(query))
            print()


def interactive_repl(inspect_mode: bool = False):
    print(BANNER)
    pipeline = CompilerPipeline()
    buffer = []

    print(f"Interactive Shell ready. Inspect mode is {'ON' if inspect_mode else 'OFF'}.")
    print("Type queries terminating with a semicolon ';' or special commands.\n")

    while True:
        try:
            prompt = "QueryLang> " if not buffer else "      ...> "
            line = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting QueryLang shell.")
            break

        clean = line.strip()
        if not buffer and clean.startswith("\\"):
            cmd = clean.lower()
            if cmd in ("\\quit", "\\exit"):
                print("Goodbye!")
                break
            elif cmd == "\\help":
                print(BANNER)
            elif cmd == "\\schema":
                print("\n" + DEFAULT_CATALOG.format_catalog())
            elif cmd in ("\\demo", "\\review3"):
                run_review3_demo()
            elif cmd == "\\benchmark":
                bench_q = """
                SELECT students.name, departments.dept_name
                FROM students
                JOIN departments ON students.branch = departments.dept_name
                WHERE students.age > (18 + 2) AND students.cgpa > 8.0;
                """
                res = run_benchmark_scale(bench_q, scales=[100, 1000, 10000])
                print(format_benchmark_report(bench_q, res))
            elif cmd == "\\test":
                run_formal_test_suite()
            elif cmd.startswith("\\dot"):
                raw_q = clean[len("\\dot"):].strip()
                if not raw_q:
                    raw_q = "SELECT name, branch FROM students WHERE age >= 20;"
                insp = pipeline.inspect_query(raw_q)
                export_dot(insp.dot_ast, "querylang_ast.dot")
                export_dot(insp.dot_plan, "querylang_plan.dot")
                print("Exported Graphviz DOT files: querylang_ast.dot, querylang_plan.dot")
            elif cmd.startswith("\\inspect"):
                raw_q = clean[len("\\inspect"):].strip()
                if raw_q:
                    inspect_and_display(pipeline, raw_q)
                else:
                    inspect_mode = not inspect_mode
                    print(f"Stage inspection toggled: {'ON' if inspect_mode else 'OFF'}.")
            else:
                print(f"Unknown command: {clean}. Type '\\help' for command list.")
            continue

        if not clean:
            continue

        buffer.append(line)
        if clean.endswith(";"):
            full_query = " ".join(buffer).strip()
            buffer.clear()
            execute_single_query(pipeline, full_query, inspect=inspect_mode)


def main():
    parser = argparse.ArgumentParser(description="QueryLang Compiler-Style Query Engine (Review 3 Final)")
    parser.add_argument("-q", "--query", type=str, help="Execute a single QueryLang query and exit")
    parser.add_argument("-i", "--inspect", action="store_true", help="Enable stage-by-stage compiler inspection")
    parser.add_argument("-d", "--demo", "--review3", dest="demo", action="store_true", help="Run Review 3 demonstration suite")
    parser.add_argument("-b", "--benchmark", action="store_true", help="Run performance benchmarks across 100, 1k, 10k rows")
    parser.add_argument("-t", "--test", action="store_true", help="Run full 25-test verification matrix")
    parser.add_argument("-s", "--schema", action="store_true", help="Display Symbol Table (Schema Catalog)")
    parser.add_argument("--dot", type=str, help="Export AST and Plan DOT files for a given query")
    parser.add_argument("-f", "--file", type=str, help="Execute queries from a file")

    args = parser.parse_args()

    pipeline = CompilerPipeline()

    if args.demo:
        run_review3_demo()
        return

    if args.benchmark:
        bench_q = """
        SELECT students.name, departments.dept_name
        FROM students
        JOIN departments ON students.branch = departments.dept_name
        WHERE students.age > (18 + 2) AND students.cgpa > 8.0;
        """
        res = run_benchmark_scale(bench_q, scales=[100, 1000, 10000])
        print(format_benchmark_report(bench_q, res))
        return

    if args.test:
        run_formal_test_suite()
        return

    if args.schema:
        print(DEFAULT_CATALOG.format_catalog())
        return

    if args.dot:
        insp = pipeline.inspect_query(args.dot)
        export_dot(insp.dot_ast, "querylang_ast.dot")
        export_dot(insp.dot_plan, "querylang_plan.dot")
        print(f"Exported DOT representations for '{args.dot}':")
        print("  - querylang_ast.dot")
        print("  - querylang_plan.dot")
        return

    if args.query:
        execute_single_query(pipeline, args.query, inspect=args.inspect)
        return

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
        queries = [q.strip() + ";" for q in content.split(";") if q.strip()]
        for q in queries:
            print(f"Executing: {q}")
            execute_single_query(pipeline, q, inspect=args.inspect)
        return

    # Default to interactive shell
    interactive_repl(inspect_mode=args.inspect)


if __name__ == '__main__':
    main()
