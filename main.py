"""
QueryLang Interactive CLI and Compiler Driver
Main entry point for BCSE307P Compiler Design Laboratory - Review 2.
Supports interactive query execution, stage-by-stage pipeline inspection,
test execution, schema catalog inspection, and automated demonstration.
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
from demo import run_demo
from tests.run_all_tests import run_formal_test_suite


BANNER = r"""
================================================================================  
   A Compiler-Style Query Processing Engine | Review 2 Core Implementation
   Student: Aman Katakwar (24BCE0160) | Guide: Prof. Ranjithkumar S
================================================================================
Commands:
  \help          - Show this help message
  \schema        - Display Schema Catalog (Symbol Table)
  \inspect <sql> - Run query with full stage-by-stage compiler inspection
  \demo          - Run the Review 2 demonstration suite
  \test          - Run the comprehensive 16-test verification matrix
  \quit or \exit - Exit the shell
================================================================================
"""


def inspect_and_display(pipeline: CompilerPipeline, query: str):
    print("\n" + "=" * 80)
    print(f"COMPILER PIPELINE STAGE-BY-STAGE INSPECTION: {query}")
    print("=" * 80)
    try:
        insp = pipeline.inspect_query(query)

        print("\n--- [STAGE 1] TOKENS (LEXICAL ANALYSIS) ---")
        for t in insp.tokens:
            print(f"  {t.format_row()}")

        print("\n--- [STAGE 2] AST (SYNTAX ANALYSIS) ---")
        print(insp.ast_tree_repr)

        print("--- [STAGE 3] SEMANTIC VALIDATION & SYMBOL BINDING ---")
        tbl = insp.validated_query.table_symbol
        cols = [f"{c.name}:{c.data_type}" for c in insp.validated_query.projected_columns]
        print(f"  Bound Table: {tbl.name}")
        print(f"  Bound Projected Columns: [{', '.join(cols)}]")
        print("  Semantic Status: VALID")

        print("\n--- [STAGE 4] LOGICAL QUERY PLAN (INTERMEDIATE CODE / IR) ---")
        print(insp.plan_tree_repr)

        print("--- [STAGE 5] EXECUTION RESULT ---")
        print(insp.result.format_table())
        print("=" * 80 + "\n")

    except QueryLangError as err:
        print("\n" + err.format_diagnostic(query))
        print("=" * 80 + "\n")


def execute_single_query(pipeline: CompilerPipeline, query: str, inspect: bool = False):
    if inspect:
        inspect_and_display(pipeline, query)
    else:
        try:
            res = pipeline.execute_query(query)
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
            elif cmd == "\\demo":
                run_demo()
            elif cmd == "\\test":
                run_formal_test_suite()
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
    parser = argparse.ArgumentParser(description="QueryLang Compiler-Style Query Engine (Review 2)")
    parser.add_argument("-q", "--query", type=str, help="Execute a single QueryLang query and exit")
    parser.add_argument("-i", "--inspect", action="store_true", help="Enable stage-by-stage compiler inspection")
    parser.add_argument("-d", "--demo", action="store_true", help="Run Review 2 demonstration")
    parser.add_argument("-t", "--test", action="store_true", help="Run full verification test matrix")
    parser.add_argument("-s", "--schema", action="store_true", help="Display Symbol Table (Schema Catalog)")
    parser.add_argument("-f", "--file", type=str, help="Execute queries from a file")

    args = parser.parse_args()

    pipeline = CompilerPipeline()

    if args.demo:
        run_demo()
        return

    if args.test:
        run_formal_test_suite()
        return

    if args.schema:
        print(DEFAULT_CATALOG.format_catalog())
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
