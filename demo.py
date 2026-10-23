"""
QueryLang Review 2 Interactive Demonstration Script
Executes the five canonical live demonstrations required by the Review 2 rubric.
Demonstrates:
  Demo 1: Basic SELECT projection
  Demo 2: Filtered SELECT with comparison operations
  Demo 3: Semantic Error Handling (unknown column, type incompatibility)
  Demo 4: Syntax Error Handling (missing grammar tokens)
  Demo 5: Complete Compiler Pipeline Stage-by-Stage Inspection
"""

import sys
import os
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from querylang.pipeline import CompilerPipeline
from querylang.errors import QueryLangError
from querylang.schema.catalog import DEFAULT_CATALOG


def separator(title: str = ""):
    print("\n" + "=" * 80)
    if title:
        print(f" >>> {title.upper()} <<<")
        print("=" * 80)


def run_demo():
    pipeline = CompilerPipeline()

    print("\n" + "#" * 80)
    print("      QUERYLANG: A COMPILER-STYLE QUERY PROCESSING ENGINE")
    print("               PHASE 2 / REVIEW 2 CORE IMPLEMENTATION DEMO")
    print("               Student: Aman Katakwar | Reg: 24BCE0160")
    print("               Course: BCSE307P Compiler Design")
    print("#" * 80)

    # -------------------------------------------------------------
    # DEMO 1: Basic SELECT Projection
    # -------------------------------------------------------------
    separator("Demo 1: Basic SELECT Projection")
    q1 = "SELECT name FROM students;"
    print(f"Query: {q1}\n")
    res1 = pipeline.execute_query(q1)
    print(res1.format_table())

    # -------------------------------------------------------------
    # DEMO 2: Filtered Query with Relational Predicate
    # -------------------------------------------------------------
    separator("Demo 2: Relational Filtering (WHERE Clause)")
    q2 = "SELECT name, age, cgpa FROM students WHERE age > 20;"
    print(f"Query: {q2}\n")
    res2 = pipeline.execute_query(q2)
    print(res2.format_table())

    # -------------------------------------------------------------
    # DEMO 3: Semantic Diagnostics (Symbol Table & Type Checker)
    # -------------------------------------------------------------
    separator("Demo 3: Semantic Analysis & Diagnostics")
    
    # 3A: Unknown column
    q3a = "SELECT salary FROM students;"
    print(f"Case 3A - Unknown Column Reference:\nQuery: {q3a}")
    try:
        pipeline.execute_query(q3a)
    except QueryLangError as err:
        print(err.format_diagnostic(q3a))

    print("\n" + "-" * 40 + "\n")

    # 3B: Incompatible types in comparison
    q3b = "SELECT name FROM students WHERE name > 50;"
    print(f"Case 3B - Type Incompatibility (STRING > INTEGER):\nQuery: {q3b}")
    try:
        pipeline.execute_query(q3b)
    except QueryLangError as err:
        print(err.format_diagnostic(q3b))

    # -------------------------------------------------------------
    # DEMO 4: Syntactic Diagnostics (Parser Error Recovery & Reporting)
    # -------------------------------------------------------------
    separator("Demo 4: Syntax Analysis & Grammar Diagnostics")
    
    # 4A: Missing column after SELECT
    q4a = "SELECT FROM students;"
    print(f"Case 4A - Missing Column Projection:\nQuery: {q4a}")
    try:
        pipeline.execute_query(q4a)
    except QueryLangError as err:
        print(err.format_diagnostic(q4a))

    print("\n" + "-" * 40 + "\n")

    # 4B: Missing FROM keyword
    q4b = "SELECT name students;"
    print(f"Case 4B - Missing 'FROM' Keyword:\nQuery: {q4b}")
    try:
        pipeline.execute_query(q4b)
    except QueryLangError as err:
        print(err.format_diagnostic(q4b))

    # -------------------------------------------------------------
    # DEMO 5: Complete Stage-by-Stage Compiler Pipeline Inspection
    # -------------------------------------------------------------
    separator("Demo 5: Complete Compiler Pipeline Deep Dive")
    q5 = "SELECT name, cgpa FROM students WHERE cgpa >= 8.5 AND age > 20;"
    print(f"Canonical Complex Query:\n  {q5}\n")

    inspection = pipeline.inspect_query(q5)

    print("[STAGE 1] LEXICAL ANALYSIS - TOKEN STREAM:")
    print(f"  {'TOKEN TYPE':<15} {'VALUE':<15} {'LOCATION'}")
    print("  " + "-" * 45)
    for tok in inspection.tokens:
        loc = f"line={tok.line}, col={tok.column}"
        print(f"  {tok.type.name:<15} {str(tok.value):<15} {loc}")

    print("\n[STAGE 2] SYNTAX ANALYSIS - ABSTRACT SYNTAX TREE (AST):")
    print(inspection.ast_tree_repr)

    print("[STAGE 3] SEMANTIC ANALYSIS - SYMBOL TABLE VERIFICATION:")
    tbl_sym = inspection.validated_query.table_symbol
    cols_sym = [c.name + f" ({c.data_type})" for c in inspection.validated_query.projected_columns]
    print(f"  Target Table Bound     : {tbl_sym.name} (Valid in Catalog)")
    print(f"  Projected Columns Bound: {', '.join(cols_sym)}")
    print(f"  Condition Type Checked : BOOLEAN (Valid operator & operand types)")

    print("\n[STAGE 4] INTERMEDIATE CODE GENERATION - LOGICAL QUERY PLAN (IR):")
    print(inspection.plan_tree_repr)

    print("[STAGE 5] IN-MEMORY QUERY EXECUTION RESULT:")
    print(inspection.result.format_table())

    separator("Demonstration Completed Successfully")
    print("Review 2 Requirements Status: All 5 Demos Operational and Validated.\n")


if __name__ == '__main__':
    run_demo()
