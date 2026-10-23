"""
================================================================================
  QUERYLANG: A COMPILER-STYLE QUERY PROCESSING ENGINE (ALL-IN-ONE CONSOLIDATED)
================================================================================
Course: BCSE307P - Compiler Design Laboratory
Student: Aman Katakwar | Reg. No.: 24BCE0160
Guide: Prof. Ranjithkumar S | Academic Year: 2026-27

This file contains the complete, self-contained implementation of the QueryLang
compiler pipeline in a single file:
  1. Diagnostic & Error System
  2. Lexical Analyzer (Tokens & Regex Scanner)
  3. Abstract Syntax Tree (AST Nodes & ASCII Visualizer)
  4. Context-Free Grammar & Recursive-Descent LL(1) Parser
  5. Symbol Table / Schema Catalog
  6. Semantic Analyzer & Static Type Checker
  7. Relational Algebra Intermediate Representation (Query Planner)
  8. In-Memory Execution Engine & ASCII Table Renderer
  9. In-Memory Datasets
 10. Automated 16-Test Verification Suite
 11. 5 Live Review 2 Demonstration Scenarios
 12. Interactive CLI & REPL

Usage:
  python all_in_one_querylang.py           # Launch Interactive REPL
  python all_in_one_querylang.py --demo    # Run Review 2 Live Demonstration
  python all_in_one_querylang.py --test    # Run Verification Matrix
  python all_in_one_querylang.py --schema  # Display Symbol Table
================================================================================
"""

import sys
import re
import argparse
from enum import Enum, auto
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set, Tuple


# ==============================================================================
# SECTION 1: DIAGNOSTIC & ERROR HIERARCHY
# ==============================================================================

class QueryLangError(Exception):
    """Base exception for all QueryLang compiler errors."""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, hint: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.hint = hint

    def format_diagnostic(self, source_query: Optional[str] = None) -> str:
        stage = self.__class__.__name__.replace("Error", "").upper()
        header = f"[{stage} ERROR]"
        location = ""
        if self.line is not None and self.column is not None:
            location = f" at Line {self.line}, Column {self.column}"
        elif self.line is not None:
            location = f" at Line {self.line}"

        lines = [f"{header}{location}: {self.message}"]
        if source_query and self.line is not None:
            query_lines = source_query.splitlines()
            if 0 <= self.line - 1 < len(query_lines):
                src_line = query_lines[self.line - 1]
                lines.append(f"  --> {src_line}")
                if self.column is not None and self.column >= 1:
                    padding = " " * (self.column + 5)
                    lines.append(f"{padding}^")

        if self.hint:
            lines.append(f"  HINT: {self.hint}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.format_diagnostic()


class LexicalError(QueryLangError):
    """Raised when an unrecognized character or malformed token is encountered."""
    pass


class SyntaxError(QueryLangError):
    """Raised when query tokens violate QueryLang context-free grammar rules."""
    pass


class SemanticError(QueryLangError):
    """Raised for schema mismatches, unknown tables/columns, or type incompatibility."""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 hint: Optional[str] = None, available_options: Optional[List[str]] = None):
        super().__init__(message, line, column, hint)
        self.available_options = available_options or []
        if self.available_options and not self.hint:
            self.hint = f"Available options: {', '.join(self.available_options)}"


class ExecutionError(QueryLangError):
    """Raised for runtime errors encountered during intermediate plan execution."""
    pass


# ==============================================================================
# SECTION 2: LEXICAL ANALYZER (TOKENS & SCANNER)
# ==============================================================================

class TokenType(Enum):
    # Keywords
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    AND = auto()
    OR = auto()
    ORDER = auto()
    BY = auto()
    LIMIT = auto()

    # Identifiers & Literals
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()

    # Comparison Operators
    EQ = auto()       # =
    NEQ = auto()      # !=
    GT = auto()       # >
    LT = auto()       # <
    GTE = auto()      # >=
    LTE = auto()      # <=

    # Delimiters / Punctuation
    COMMA = auto()     # ,
    SEMICOLON = auto() # ;
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    STAR = auto()      # *

    # Special
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"

    def format_row(self) -> str:
        return f"{self.type.name:<14} {str(self.value):<16} line={self.line:<3} col={self.column:<3}"


class Lexer:
    KEYWORDS = {
        'SELECT': TokenType.SELECT,
        'FROM': TokenType.FROM,
        'WHERE': TokenType.WHERE,
        'AND': TokenType.AND,
        'OR': TokenType.OR,
        'ORDER': TokenType.ORDER,
        'BY': TokenType.BY,
        'LIMIT': TokenType.LIMIT,
        'TRUE': TokenType.BOOLEAN,
        'FALSE': TokenType.BOOLEAN,
    }

    TOKEN_SPECIFICATION = [
        ('WHITESPACE', r'[ \t\r\n]+'),
        ('COMMENT',    r'--[^\r\n]*'),
        ('FLOAT',      r'\d+\.\d+'),
        ('INTEGER',    r'\d+'),
        ('STRING',     r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''),
        ('GTE',        r'>='),
        ('LTE',        r'<='),
        ('NEQ',        r'!='),
        ('GT',         r'>'),
        ('LT',         r'<'),
        ('EQ',         r'='),
        ('COMMA',      r','),
        ('SEMICOLON',  r';'),
        ('LPAREN',     r'\('),
        ('RPAREN',     r'\)'),
        ('STAR',       r'\*'),
        ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
    ]

    MASTER_REGEX = re.compile(
        '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
    )

    def __init__(self, source_code: str):
        self.source_code = source_code

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        pos = 0
        line = 1
        line_start = 0

        for match in self.MASTER_REGEX.finditer(self.source_code):
            if match.start() != pos:
                bad_char = self.source_code[pos:match.start()]
                col = pos - line_start + 1
                raise LexicalError(
                    f"Invalid character sequence {bad_char!r}",
                    line=line,
                    column=col,
                    hint="Remove or replace the unsupported character."
                )

            kind = match.lastgroup
            raw_val = match.group()
            col = match.start() - line_start + 1

            if kind == 'WHITESPACE':
                newlines = raw_val.count('\n')
                if newlines > 0:
                    line += newlines
                    line_start = match.start() + raw_val.rfind('\n') + 1
            elif kind == 'COMMENT':
                pass
            else:
                upper_val = raw_val.upper()
                if kind == 'IDENTIFIER' and upper_val in self.KEYWORDS:
                    token_type = self.KEYWORDS[upper_val]
                    if token_type == TokenType.BOOLEAN:
                        parsed_val = (upper_val == 'TRUE')
                        tokens.append(Token(TokenType.BOOLEAN, parsed_val, line, col))
                    else:
                        tokens.append(Token(token_type, upper_val, line, col))
                elif kind == 'IDENTIFIER':
                    tokens.append(Token(TokenType.IDENTIFIER, raw_val, line, col))
                elif kind == 'INTEGER':
                    tokens.append(Token(TokenType.INTEGER, int(raw_val), line, col))
                elif kind == 'FLOAT':
                    tokens.append(Token(TokenType.FLOAT, float(raw_val), line, col))
                elif kind == 'STRING':
                    unescaped = raw_val[1:-1].replace(r'\"', '"').replace(r"\'", "'")
                    tokens.append(Token(TokenType.STRING, unescaped, line, col))
                elif kind == 'GTE':
                    tokens.append(Token(TokenType.GTE, '>=', line, col))
                elif kind == 'LTE':
                    tokens.append(Token(TokenType.LTE, '<=', line, col))
                elif kind == 'NEQ':
                    tokens.append(Token(TokenType.NEQ, '!=', line, col))
                elif kind == 'GT':
                    tokens.append(Token(TokenType.GT, '>', line, col))
                elif kind == 'LT':
                    tokens.append(Token(TokenType.LT, '<', line, col))
                elif kind == 'EQ':
                    tokens.append(Token(TokenType.EQ, '=', line, col))
                elif kind == 'COMMA':
                    tokens.append(Token(TokenType.COMMA, ',', line, col))
                elif kind == 'SEMICOLON':
                    tokens.append(Token(TokenType.SEMICOLON, ';', line, col))
                elif kind == 'LPAREN':
                    tokens.append(Token(TokenType.LPAREN, '(', line, col))
                elif kind == 'RPAREN':
                    tokens.append(Token(TokenType.RPAREN, ')', line, col))
                elif kind == 'STAR':
                    tokens.append(Token(TokenType.STAR, '*', line, col))

            pos = match.end()

        if pos != len(self.source_code):
            bad_char = self.source_code[pos:]
            col = pos - line_start + 1
            raise LexicalError(
                f"Invalid character sequence {bad_char!r}",
                line=line,
                column=col,
                hint="Check for unexpected trailing characters."
            )

        final_col = (len(self.source_code) - line_start) + 1
        tokens.append(Token(TokenType.EOF, "", line, final_col))
        return tokens


# ==============================================================================
# SECTION 3: ABSTRACT SYNTAX TREE (AST NODES)
# ==============================================================================

class ASTNode(ABC):
    @abstractmethod
    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        pass


class LiteralNode(ASTNode):
    def __init__(self, value: Any, literal_type: str, line: int = 1, column: int = 1):
        self.value = value
        self.literal_type = literal_type
        self.line = line
        self.column = column

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        return f"{prefix}{marker}LiteralNode({self.value!r} : {self.literal_type})\n"

    def __repr__(self) -> str:
        return f"LiteralNode({self.value!r}, type={self.literal_type})"


class ColumnNode(ASTNode):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        self.name = name
        self.line = line
        self.column = column

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        return f"{prefix}{marker}ColumnNode({self.name})\n"

    def __repr__(self) -> str:
        return f"ColumnNode({self.name})"


class TableNode(ASTNode):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        self.name = name
        self.line = line
        self.column = column

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        return f"{prefix}{marker}TableNode({self.name})\n"

    def __repr__(self) -> str:
        return f"TableNode({self.name})"


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode, line: int = 1, column: int = 1):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line
        self.column = column

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        sub_prefix = prefix + ("    " if is_last else "|   ")
        res = f"{prefix}{marker}BinaryOpNode({self.operator})\n"
        res += self.left.tree_repr(sub_prefix, False)
        res += self.right.tree_repr(sub_prefix, True)
        return res

    def __repr__(self) -> str:
        return f"BinaryOpNode({self.left} {self.operator} {self.right})"


class SelectQueryNode(ASTNode):
    def __init__(
        self,
        columns: List[ColumnNode],
        is_wildcard: bool,
        table: TableNode,
        where_condition: Optional[ASTNode] = None,
        order_by_column: Optional[ColumnNode] = None,
        limit_count: Optional[int] = None,
        line: int = 1,
        column: int = 1
    ):
        self.columns = columns
        self.is_wildcard = is_wildcard
        self.table = table
        self.where_condition = where_condition
        self.order_by_column = order_by_column
        self.limit_count = limit_count
        self.line = line
        self.column = column

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        res = "SelectQueryNode\n"
        cols_str = "*" if self.is_wildcard else ", ".join(c.name for c in self.columns)
        res += f"|-- Projected Columns: [{cols_str}]\n"
        res += f"|-- Source Table: {self.table.name}\n"
        has_more = (self.order_by_column is not None) or (self.limit_count is not None)
        if self.where_condition:
            res += f"|-- WHERE Condition:\n"
            condition_prefix = "|   " if has_more else "    "
            res += self.where_condition.tree_repr(condition_prefix, True)
        else:
            res += f"|-- WHERE Condition: (None)\n"

        if self.order_by_column:
            limit_more = self.limit_count is not None
            res += f"{'|--' if limit_more else '\\--'} ORDER BY: {self.order_by_column.name}\n"

        if self.limit_count is not None:
            res += f"\\-- LIMIT: {self.limit_count}\n"
        return res

    def __repr__(self) -> str:
        cols = "*" if self.is_wildcard else [c.name for c in self.columns]
        return f"SelectQueryNode(table={self.table.name}, columns={cols}, where={self.where_condition})"


# ==============================================================================
# SECTION 4: RECURSIVE-DESCENT LL(1) PARSER
# ==============================================================================

class Parser:
    def __init__(self, tokens: List[Token], source_query: Optional[str] = None):
        self.tokens = tokens
        self.cursor = 0
        self.source_query = source_query

    @property
    def current_token(self) -> Token:
        if self.cursor < len(self.tokens):
            return self.tokens[self.cursor]
        return self.tokens[-1]

    def match(self, *expected_types: TokenType) -> bool:
        return self.current_token.type in expected_types

    def consume(self, expected_type: TokenType, error_msg: Optional[str] = None) -> Token:
        tok = self.current_token
        if tok.type == expected_type:
            self.cursor += 1
            return tok

        found_desc = tok.type.name if tok.type != TokenType.EOF else "End of Input"
        expected_desc = expected_type.name
        msg = error_msg or f"Expected '{expected_desc}', but found '{found_desc}' with value {tok.value!r}."
        raise SyntaxError(
            msg,
            line=tok.line,
            column=tok.column,
            hint=f"Check syntax around '{tok.value}'."
        )

    def parse(self) -> SelectQueryNode:
        if self.match(TokenType.EOF):
            raise SyntaxError("Query is empty. Expected 'SELECT ...'", line=1, column=1)

        node = self.parse_query()
        self.consume(TokenType.SEMICOLON, "Expected ';' to terminate the query.")

        if not self.match(TokenType.EOF):
            extra_tok = self.current_token
            raise SyntaxError(
                f"Unexpected token {extra_tok.value!r} after query terminator ';'.",
                line=extra_tok.line,
                column=extra_tok.column,
                hint="Only one statement per query is supported. Remove trailing text."
            )
        return node

    def parse_query(self) -> SelectQueryNode:
        select_tok = self.consume(TokenType.SELECT, "A QueryLang statement must begin with 'SELECT'.")
        columns, is_wildcard = self.parse_column_list()
        self.consume(TokenType.FROM, "Expected 'FROM' after column list.")
        table_tok = self.consume(TokenType.IDENTIFIER, "Expected table name after 'FROM'.")
        table_node = TableNode(table_tok.value, line=table_tok.line, column=table_tok.column)

        where_cond: Optional[ASTNode] = None
        if self.match(TokenType.WHERE):
            self.consume(TokenType.WHERE)
            where_cond = self.parse_condition()

        order_col: Optional[ColumnNode] = None
        if self.match(TokenType.ORDER):
            self.consume(TokenType.ORDER)
            self.consume(TokenType.BY, "Expected 'BY' after 'ORDER'.")
            col_tok = self.consume(TokenType.IDENTIFIER, "Expected column name after 'ORDER BY'.")
            order_col = ColumnNode(col_tok.value, line=col_tok.line, column=col_tok.column)

        limit_count: Optional[int] = None
        if self.match(TokenType.LIMIT):
            self.consume(TokenType.LIMIT)
            limit_tok = self.consume(TokenType.INTEGER, "Expected integer count after 'LIMIT'.")
            limit_count = int(limit_tok.value)

        return SelectQueryNode(
            columns=columns,
            is_wildcard=is_wildcard,
            table=table_node,
            where_condition=where_cond,
            order_by_column=order_col,
            limit_count=limit_count,
            line=select_tok.line,
            column=select_tok.column
        )

    def parse_column_list(self) -> Tuple[List[ColumnNode], bool]:
        if self.match(TokenType.STAR):
            self.consume(TokenType.STAR)
            return [], True

        columns: List[ColumnNode] = []
        if not self.match(TokenType.IDENTIFIER):
            curr = self.current_token
            raise SyntaxError(
                f"Expected column name or '*' after SELECT, but found '{curr.value}'.",
                line=curr.line,
                column=curr.column,
                hint="Specify column identifiers separated by commas, or '*'."
            )

        col_tok = self.consume(TokenType.IDENTIFIER)
        columns.append(ColumnNode(col_tok.value, line=col_tok.line, column=col_tok.column))

        while self.match(TokenType.COMMA):
            self.consume(TokenType.COMMA)
            col_tok = self.consume(TokenType.IDENTIFIER, "Expected column name after ','.")
            columns.append(ColumnNode(col_tok.value, line=col_tok.line, column=col_tok.column))

        return columns, False

    def parse_condition(self) -> ASTNode:
        return self.parse_or_expr()

    def parse_or_expr(self) -> ASTNode:
        left = self.parse_and_expr()
        while self.match(TokenType.OR):
            op_tok = self.consume(TokenType.OR)
            right = self.parse_and_expr()
            left = BinaryOpNode(left, 'OR', right, line=op_tok.line, column=op_tok.column)
        return left

    def parse_and_expr(self) -> ASTNode:
        left = self.parse_comparison()
        while self.match(TokenType.AND):
            op_tok = self.consume(TokenType.AND)
            right = self.parse_comparison()
            left = BinaryOpNode(left, 'AND', right, line=op_tok.line, column=op_tok.column)
        return left

    def parse_comparison(self) -> ASTNode:
        left = self.parse_primary_expr()
        comp_ops = {
            TokenType.EQ: '=',
            TokenType.NEQ: '!=',
            TokenType.GT: '>',
            TokenType.LT: '<',
            TokenType.GTE: '>=',
            TokenType.LTE: '<='
        }
        if self.match(*comp_ops.keys()):
            op_tok = self.current_token
            op_str = comp_ops[op_tok.type]
            self.consume(op_tok.type)
            right = self.parse_primary_expr()
            return BinaryOpNode(left, op_str, right, line=op_tok.line, column=op_tok.column)
        return left

    def parse_primary_expr(self) -> ASTNode:
        curr = self.current_token
        if self.match(TokenType.LPAREN):
            self.consume(TokenType.LPAREN)
            node = self.parse_condition()
            self.consume(TokenType.RPAREN, "Expected closing ')' for condition.")
            return node
        if self.match(TokenType.IDENTIFIER):
            self.consume(TokenType.IDENTIFIER)
            return ColumnNode(curr.value, line=curr.line, column=curr.column)
        if self.match(TokenType.INTEGER):
            self.consume(TokenType.INTEGER)
            return LiteralNode(curr.value, 'INTEGER', line=curr.line, column=curr.column)
        if self.match(TokenType.FLOAT):
            self.consume(TokenType.FLOAT)
            return LiteralNode(curr.value, 'FLOAT', line=curr.line, column=curr.column)
        if self.match(TokenType.STRING):
            self.consume(TokenType.STRING)
            return LiteralNode(curr.value, 'STRING', line=curr.line, column=curr.column)
        if self.match(TokenType.BOOLEAN):
            self.consume(TokenType.BOOLEAN)
            return LiteralNode(curr.value, 'BOOLEAN', line=curr.line, column=curr.column)

        raise SyntaxError(
            f"Expected column identifier, literal value, or '(', but found {curr.value!r}.",
            line=curr.line,
            column=curr.column,
            hint="Ensure expressions inside WHERE conditions contain valid operands."
        )


# ==============================================================================
# SECTION 5: SYMBOL TABLE / SCHEMA CATALOG
# ==============================================================================

@dataclass
class ColumnSymbol:
    name: str
    data_type: str
    description: str = ""


@dataclass
class TableSymbol:
    name: str
    columns: Dict[str, ColumnSymbol]

    def add_column(self, name: str, data_type: str, description: str = ""):
        self.columns[name.lower()] = ColumnSymbol(name=name, data_type=data_type.upper(), description=description)

    def has_column(self, name: str) -> bool:
        return name.lower() in self.columns

    def get_column(self, name: str) -> Optional[ColumnSymbol]:
        return self.columns.get(name.lower())

    def get_column_names(self) -> List[str]:
        return [c.name for c in self.columns.values()]


class SchemaCatalog:
    def __init__(self):
        self.tables: Dict[str, TableSymbol] = {}
        self._init_default_schema()

    def _init_default_schema(self):
        students = TableSymbol(name="students", columns={})
        students.add_column("id", "INTEGER", "Unique student identifier")
        students.add_column("name", "STRING", "Full name of the student")
        students.add_column("age", "INTEGER", "Age in years")
        students.add_column("branch", "STRING", "Academic department")
        students.add_column("cgpa", "FLOAT", "Cumulative Grade Point Average")
        self.add_table(students)

        departments = TableSymbol(name="departments", columns={})
        departments.add_column("dept_id", "INTEGER", "Department ID")
        departments.add_column("dept_name", "STRING", "Name of the department")
        departments.add_column("hod", "STRING", "Head of department name")
        departments.add_column("building", "STRING", "Campus location")
        self.add_table(departments)

    def add_table(self, table: TableSymbol):
        self.tables[table.name.lower()] = table

    def has_table(self, name: str) -> bool:
        return name.lower() in self.tables

    def get_table(self, name: str) -> Optional[TableSymbol]:
        return self.tables.get(name.lower())

    def get_table_names(self) -> List[str]:
        return [t.name for t in self.tables.values()]

    def format_catalog(self) -> str:
        lines = ["=== QueryLang Schema Catalog (Symbol Table) ==="]
        for tbl_name, tbl in self.tables.items():
            lines.append(f"Table: {tbl.name}")
            lines.append(f"  {'Column':<15} {'Type':<12} {'Description'}")
            lines.append(f"  {'-'*15} {'-'*12} {'-'*25}")
            for col in tbl.columns.values():
                lines.append(f"  {col.name:<15} {col.data_type:<12} {col.description}")
            lines.append("")
        return "\n".join(lines)


# ==============================================================================
# SECTION 6: SEMANTIC ANALYZER & STATIC TYPE CHECKER
# ==============================================================================

class TypeChecker:
    NUMERIC_TYPES: Set[str] = {"INTEGER", "FLOAT"}

    @classmethod
    def check_comparison(cls, op: str, left_type: str, right_type: str, line: int = 1, column: int = 1) -> str:
        if op in {'=', '!='}:
            if left_type in cls.NUMERIC_TYPES and right_type in cls.NUMERIC_TYPES:
                return "BOOLEAN"
            if left_type == right_type:
                return "BOOLEAN"
            raise SemanticError(
                f"Operator '{op}' cannot be applied to types {left_type} and {right_type}.",
                line=line, column=column,
                hint="Ensure both operands have matching or compatible types."
            )

        if op in {'>', '<', '>=', '<='}:
            if left_type in cls.NUMERIC_TYPES and right_type in cls.NUMERIC_TYPES:
                return "BOOLEAN"
            if left_type == "STRING" and right_type == "STRING":
                return "BOOLEAN"
            raise SemanticError(
                f"Operator '{op}' cannot be applied to {left_type} and {right_type}.",
                line=line, column=column,
                hint=f"Relational ordering '{op}' requires numeric or string operands of compatible types."
            )

        if op in {'AND', 'OR'}:
            if left_type == "BOOLEAN" and right_type == "BOOLEAN":
                return "BOOLEAN"
            raise SemanticError(
                f"Logical operator '{op}' requires BOOLEAN operands, got {left_type} and {right_type}.",
                line=line, column=column,
                hint="Use comparisons or boolean expressions with AND/OR."
            )

        raise SemanticError(f"Unknown operator '{op}'.", line=line, column=column)


@dataclass
class ValidatedQuery:
    ast: SelectQueryNode
    table_symbol: TableSymbol
    projected_columns: List[ColumnSymbol]
    is_wildcard: bool
    order_by_symbol: Optional[ColumnSymbol]
    limit: Optional[int]


class SemanticAnalyzer:
    def __init__(self, catalog: Optional[SchemaCatalog] = None):
        self.catalog = catalog or SchemaCatalog()
        self.current_table: Optional[TableSymbol] = None

    def analyze(self, query_node: SelectQueryNode) -> ValidatedQuery:
        table_name = query_node.table.name
        if not self.catalog.has_table(table_name):
            available = self.catalog.get_table_names()
            raise SemanticError(
                f"Table {table_name!r} does not exist.",
                line=query_node.table.line,
                column=query_node.table.column,
                hint=f"Available tables: {', '.join(available)}",
                available_options=available
            )

        self.current_table = self.catalog.get_table(table_name)
        assert self.current_table is not None

        projected_symbols: List[ColumnSymbol] = []
        if query_node.is_wildcard:
            for col_sym in self.current_table.columns.values():
                projected_symbols.append(col_sym)
        else:
            for col_node in query_node.columns:
                if not self.current_table.has_column(col_node.name):
                    avail_cols = self.current_table.get_column_names()
                    raise SemanticError(
                        f"Column {col_node.name!r} does not exist in table {self.current_table.name!r}.",
                        line=col_node.line,
                        column=col_node.column,
                        hint=f"Available columns in '{self.current_table.name}': {', '.join(avail_cols)}",
                        available_options=avail_cols
                    )
                projected_symbols.append(self.current_table.get_column(col_node.name))

        if query_node.where_condition:
            cond_type = self._validate_expression(query_node.where_condition)
            if cond_type != "BOOLEAN":
                raise SemanticError(
                    f"WHERE condition must evaluate to BOOLEAN, but evaluated to {cond_type}.",
                    line=query_node.where_condition.line,
                    column=query_node.where_condition.column,
                    hint="Ensure conditions use comparison operators or booleans."
                )

        order_symbol: Optional[ColumnSymbol] = None
        if query_node.order_by_column:
            col_name = query_node.order_by_column.name
            if not self.current_table.has_column(col_name):
                avail_cols = self.current_table.get_column_names()
                raise SemanticError(
                    f"ORDER BY column {col_name!r} does not exist in table {self.current_table.name!r}.",
                    line=query_node.order_by_column.line,
                    column=query_node.order_by_column.column,
                    hint=f"Available columns: {', '.join(avail_cols)}",
                    available_options=avail_cols
                )
            order_symbol = self.current_table.get_column(col_name)

        if query_node.limit_count is not None and query_node.limit_count < 0:
            raise SemanticError(
                f"LIMIT value cannot be negative: {query_node.limit_count}",
                line=query_node.line,
                column=query_node.column,
                hint="LIMIT must be a non-negative integer."
            )

        return ValidatedQuery(
            ast=query_node,
            table_symbol=self.current_table,
            projected_columns=projected_symbols,
            is_wildcard=query_node.is_wildcard,
            order_by_symbol=order_symbol,
            limit=query_node.limit_count
        )

    def _validate_expression(self, node: ASTNode) -> str:
        if isinstance(node, ColumnNode):
            if not self.current_table.has_column(node.name):
                avail_cols = self.current_table.get_column_names()
                raise SemanticError(
                    f"Column {node.name!r} does not exist in table {self.current_table.name!r}.",
                    line=node.line,
                    column=node.column,
                    hint=f"Available columns: {', '.join(avail_cols)}",
                    available_options=avail_cols
                )
            col_sym = self.current_table.get_column(node.name)
            return col_sym.data_type

        if isinstance(node, LiteralNode):
            return node.literal_type

        if isinstance(node, BinaryOpNode):
            left_type = self._validate_expression(node.left)
            right_type = self._validate_expression(node.right)
            return TypeChecker.check_comparison(node.operator, left_type, right_type, line=node.line, column=node.column)

        raise SemanticError(f"Unexpected AST node in condition: {node}", line=node.line, column=node.column)


# ==============================================================================
# SECTION 7: RELATIONAL ALGEBRA IR & QUERY PLANNER
# ==============================================================================

class PlanNode(ABC):
    @abstractmethod
    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        pass


class ScanNode(PlanNode):
    def __init__(self, table_name: str):
        self.table_name = table_name

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        return f"{prefix}{marker}SCAN [{self.table_name}]\n"

    def __repr__(self) -> str:
        return f"ScanNode({self.table_name})"


class FilterNode(PlanNode):
    def __init__(self, child: PlanNode, predicate: ASTNode):
        self.child = child
        self.predicate = predicate

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        sub_prefix = prefix + ("    " if is_last else "|   ")
        pred_repr = str(self.predicate)
        res = f"{prefix}{marker}FILTER [{pred_repr}]\n"
        res += self.child.tree_repr(sub_prefix, True)
        return res

    def __repr__(self) -> str:
        return f"FilterNode(pred={self.predicate}, child={self.child})"


class ProjectNode(PlanNode):
    def __init__(self, child: PlanNode, columns: List[str]):
        self.child = child
        self.columns = columns

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        sub_prefix = prefix + ("    " if is_last else "|   ")
        cols_repr = ", ".join(self.columns)
        res = f"{prefix}{marker}PROJECT [{cols_repr}]\n"
        res += self.child.tree_repr(sub_prefix, True)
        return res

    def __repr__(self) -> str:
        return f"ProjectNode(cols={self.columns}, child={self.child})"


class SortNode(PlanNode):
    def __init__(self, child: PlanNode, column: str, ascending: bool = True):
        self.child = child
        self.column = column
        self.ascending = ascending

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        sub_prefix = prefix + ("    " if is_last else "|   ")
        order = "ASC" if self.ascending else "DESC"
        res = f"{prefix}{marker}SORT [{self.column} {order}]\n"
        res += self.child.tree_repr(sub_prefix, True)
        return res


class LimitNode(PlanNode):
    def __init__(self, child: PlanNode, count: int):
        self.child = child
        self.count = count

    def tree_repr(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "\\-- " if is_last else "|-- "
        sub_prefix = prefix + ("    " if is_last else "|   ")
        res = f"{prefix}{marker}LIMIT [{self.count}]\n"
        res += self.child.tree_repr(sub_prefix, True)
        return res


class QueryPlanner:
    @classmethod
    def generate_plan(cls, validated_query: ValidatedQuery) -> PlanNode:
        table_name = validated_query.table_symbol.name
        current_node: PlanNode = ScanNode(table_name)
        if validated_query.ast.where_condition:
            current_node = FilterNode(child=current_node, predicate=validated_query.ast.where_condition)

        col_names = [c.name for c in validated_query.projected_columns]
        current_node = ProjectNode(child=current_node, columns=col_names)

        if validated_query.order_by_symbol:
            current_node = SortNode(child=current_node, column=validated_query.order_by_symbol.name)

        if validated_query.limit is not None:
            current_node = LimitNode(child=current_node, count=validated_query.limit)

        return current_node


# ==============================================================================
# SECTION 8: IN-MEMORY EXECUTION ENGINE
# ==============================================================================

class ExpressionEvaluator:
    @classmethod
    def evaluate(cls, node: ASTNode, row: Dict[str, Any]) -> Any:
        if isinstance(node, ColumnNode):
            target = node.name.lower()
            for key, val in row.items():
                if key.lower() == target:
                    return val
            raise ExecutionError(f"Runtime column '{node.name}' not found in record.")

        if isinstance(node, LiteralNode):
            return node.value

        if isinstance(node, BinaryOpNode):
            op = node.operator
            if op == 'AND':
                left_val = cls.evaluate(node.left, row)
                if not bool(left_val):
                    return False
                return bool(cls.evaluate(node.right, row))

            if op == 'OR':
                left_val = cls.evaluate(node.left, row)
                if bool(left_val):
                    return True
                return bool(cls.evaluate(node.right, row))

            left_val = cls.evaluate(node.left, row)
            right_val = cls.evaluate(node.right, row)

            if op == '=':  return left_val == right_val
            if op == '!=': return left_val != right_val
            if op == '>':  return left_val > right_val
            if op == '<':  return left_val < right_val
            if op == '>=': return left_val >= right_val
            if op == '<=': return left_val <= right_val
            raise ExecutionError(f"Unsupported runtime comparison operator: {op}")

        raise ExecutionError(f"Cannot evaluate AST node of type {type(node).__name__}")


@dataclass
class QueryResult:
    columns: List[str]
    rows: List[Dict[str, Any]]
    scanned_count: int
    filtered_count: int
    returned_count: int

    def format_table(self) -> str:
        if not self.columns:
            return "(No columns selected)\n0 rows returned."

        col_widths = {col: max(len(col), 6) for col in self.columns}
        for row in self.rows:
            for col in self.columns:
                val_str = str(row.get(col, ""))
                if len(val_str) > col_widths[col]:
                    col_widths[col] = len(val_str)

        header_parts = [f" {col.upper():<{col_widths[col]}} " for col in self.columns]
        header = "|" + "|".join(header_parts) + "|"
        divider = "+" + "+".join(["-" * (col_widths[col] + 2) for col in self.columns]) + "+"

        lines = [divider, header, divider]
        if not self.rows:
            empty_msg = "(Empty set / 0 rows matched)"
            lines.append(f"| {empty_msg:<{len(header) - 4}} |")
        else:
            for row in self.rows:
                row_parts = [f" {str(row.get(col, '')):<{col_widths[col]}} " for col in self.columns]
                lines.append("|" + "|".join(row_parts) + "|")

        lines.append(divider)
        lines.append(f"{self.returned_count} row(s) in set (Scanned: {self.scanned_count}, Filtered: {self.filtered_count})")
        return "\n".join(lines)


STUDENTS_DATA = [
    {"id": 1, "name": "Asha",    "age": 21, "branch": "CSE",   "cgpa": 8.7},
    {"id": 2, "name": "Riya",    "age": 19, "branch": "ECE",   "cgpa": 8.2},
    {"id": 3, "name": "Rahul",   "age": 22, "branch": "CSE",   "cgpa": 9.1},
    {"id": 4, "name": "Vikram",  "age": 20, "branch": "MECH",  "cgpa": 7.8},
    {"id": 5, "name": "Pooja",   "age": 21, "branch": "IT",    "cgpa": 8.9},
    {"id": 6, "name": "Ananya",  "age": 23, "branch": "CSE",   "cgpa": 9.4},
    {"id": 7, "name": "Karthik", "age": 20, "branch": "CIVIL", "cgpa": 6.9},
]

DEPARTMENTS_DATA = [
    {"dept_id": 101, "dept_name": "CSE", "hod": "Dr. Sharma", "building": "Technology Tower"},
    {"dept_id": 102, "dept_name": "ECE", "hod": "Dr. Raman",  "building": "Silver Jubilee Tower"},
    {"dept_id": 103, "dept_name": "MECH","hod": "Dr. Patel",  "building": "Main Building"},
]


class ExecutionEngine:
    def __init__(self, database: Optional[Dict[str, List[Dict[str, Any]]]] = None):
        self.database = database or {
            "students": [dict(r) for r in STUDENTS_DATA],
            "departments": [dict(r) for r in DEPARTMENTS_DATA],
        }
        self.scanned_count = 0
        self.filtered_count = 0

    def execute(self, plan: PlanNode) -> QueryResult:
        self.scanned_count = 0
        self.filtered_count = 0
        rows, columns = self._execute_node(plan)
        return QueryResult(
            columns=columns,
            rows=rows,
            scanned_count=self.scanned_count,
            filtered_count=self.filtered_count,
            returned_count=len(rows)
        )

    def _execute_node(self, node: PlanNode) -> Tuple[List[Dict[str, Any]], List[str]]:
        if isinstance(node, ScanNode):
            tbl = node.table_name.lower()
            if tbl not in self.database:
                raise ExecutionError(f"Database table '{node.table_name}' not found.")
            rows = [dict(r) for r in self.database[tbl]]
            self.scanned_count = len(rows)
            cols = list(rows[0].keys()) if rows else []
            return rows, cols

        if isinstance(node, FilterNode):
            child_rows, cols = self._execute_node(node.child)
            filtered = [r for r in child_rows if bool(ExpressionEvaluator.evaluate(node.predicate, r))]
            self.filtered_count = len(filtered)
            return filtered, cols

        if isinstance(node, ProjectNode):
            child_rows, _ = self._execute_node(node.child)
            projected = []
            for r in child_rows:
                new_row = {}
                for col in node.columns:
                    target = col.lower()
                    matched_val = None
                    for k, v in r.items():
                        if k.lower() == target:
                            matched_val = v
                            break
                    new_row[col] = matched_val
                projected.append(new_row)
            return projected, node.columns

        if isinstance(node, SortNode):
            child_rows, cols = self._execute_node(node.child)
            target = node.column.lower()
            def sort_key(row):
                for k, v in row.items():
                    if k.lower() == target: return v
                return None
            sorted_rows = sorted(child_rows, key=sort_key, reverse=not node.ascending)
            return sorted_rows, cols

        if isinstance(node, LimitNode):
            child_rows, cols = self._execute_node(node.child)
            return child_rows[:node.count], cols

        raise ExecutionError(f"Unsupported plan operator node: {type(node).__name__}")


# ==============================================================================
# SECTION 9: UNIFIED COMPILER PIPELINE
# ==============================================================================

@dataclass
class PipelineInspection:
    source_query: str
    tokens: List[Token]
    ast: SelectQueryNode
    ast_tree_repr: str
    validated_query: ValidatedQuery
    plan: PlanNode
    plan_tree_repr: str
    result: QueryResult


class CompilerPipeline:
    def __init__(self):
        self.catalog = SchemaCatalog()
        self.semantic_analyzer = SemanticAnalyzer(self.catalog)
        self.planner = QueryPlanner()
        self.execution_engine = ExecutionEngine()

    def execute_query(self, query_str: str) -> QueryResult:
        inspection = self.inspect_query(query_str)
        return inspection.result

    def inspect_query(self, query_str: str) -> PipelineInspection:
        # Stage 1: Lexical Analysis
        lexer = Lexer(query_str)
        tokens = lexer.tokenize()

        # Stage 2: Syntax Analysis (Parser)
        parser = Parser(tokens, source_query=query_str)
        ast = parser.parse()
        ast_tree = ast.tree_repr()

        # Stage 3: Semantic Analysis & Symbol Binding
        validated = self.semantic_analyzer.analyze(ast)

        # Stage 4: Logical Query Planning (IR)
        plan = self.planner.generate_plan(validated)
        plan_tree = plan.tree_repr()

        # Stage 5: In-Memory Execution
        result = self.execution_engine.execute(plan)

        return PipelineInspection(
            source_query=query_str,
            tokens=tokens,
            ast=ast,
            ast_tree_repr=ast_tree,
            validated_query=validated,
            plan=plan,
            plan_tree_repr=plan_tree,
            result=result
        )


# ==============================================================================
# SECTION 10: DEMONSTRATION & VERIFICATION MATRIX
# ==============================================================================

def run_demo():
    pipeline = CompilerPipeline()
    print("\n" + "=" * 80)
    print("      QUERYLANG COMPILER ENGINE - REVIEW 2 LIVE DEMONSTRATION")
    print("      Student: Aman Katakwar (24BCE0160) | Guide: Prof. Ranjithkumar S")
    print("=" * 80)

    # Demo 1
    print("\n>>> DEMO 1: BASIC SELECT PROJECTION <<<")
    q1 = "SELECT name FROM students;"
    print(f"Query: {q1}\n" + pipeline.execute_query(q1).format_table())

    # Demo 2
    print("\n>>> DEMO 2: RELATIONAL FILTERING (WHERE CLAUSE) <<<")
    q2 = "SELECT name, age, cgpa FROM students WHERE age > 20;"
    print(f"Query: {q2}\n" + pipeline.execute_query(q2).format_table())

    # Demo 3
    print("\n>>> DEMO 3: SEMANTIC DIAGNOSTICS <<<")
    q3a = "SELECT salary FROM students;"
    print(f"Case 3A (Unknown Column): {q3a}")
    try: pipeline.execute_query(q3a)
    except QueryLangError as e: print(e.format_diagnostic(q3a))

    q3b = "SELECT name FROM students WHERE name > 50;"
    print(f"\nCase 3B (Type Mismatch STRING > INT): {q3b}")
    try: pipeline.execute_query(q3b)
    except QueryLangError as e: print(e.format_diagnostic(q3b))

    # Demo 4
    print("\n>>> DEMO 4: SYNTACTIC DIAGNOSTICS <<<")
    q4a = "SELECT FROM students;"
    print(f"Case 4A (Missing Projection): {q4a}")
    try: pipeline.execute_query(q4a)
    except QueryLangError as e: print(e.format_diagnostic(q4a))

    q4b = "SELECT name students;"
    print(f"\nCase 4B (Missing FROM): {q4b}")
    try: pipeline.execute_query(q4b)
    except QueryLangError as e: print(e.format_diagnostic(q4b))

    # Demo 5
    print("\n>>> DEMO 5: COMPLETE STAGE-BY-STAGE COMPILER PIPELINE DEEP DIVE <<<")
    q5 = "SELECT name, cgpa FROM students WHERE cgpa >= 8.5 AND age > 20;"
    print(f"Canonical Complex Query: {q5}\n")
    insp = pipeline.inspect_query(q5)

    print("[STAGE 1] TOKEN STREAM:")
    for t in insp.tokens: print(f"  {t.format_row()}")

    print("\n[STAGE 2] ABSTRACT SYNTAX TREE (AST):")
    print(insp.ast_tree_repr)

    print("[STAGE 3] SEMANTIC SYMBOL BINDING:")
    cols = [f"{c.name}:{c.data_type}" for c in insp.validated_query.projected_columns]
    print(f"  Table: {insp.validated_query.table_symbol.name} | Columns: [{', '.join(cols)}] | Status: VALID")

    print("\n[STAGE 4] LOGICAL QUERY PLAN (IR):")
    print(insp.plan_tree_repr)

    print("[STAGE 5] EXECUTION RESULT:")
    print(insp.result.format_table())
    print("\n" + "=" * 80 + "\n")


def run_tests():
    pipeline = CompilerPipeline()
    test_matrix = [
        ("T-01", "Basic SELECT Projection", "SELECT name FROM students;", lambda r: r.returned_count == 7),
        ("T-02", "Multi-column Projection", "SELECT name, cgpa FROM students;", lambda r: len(r.columns) == 2),
        ("T-03", "WHERE Relational Filter", "SELECT name FROM students WHERE age > 20;", lambda r: r.returned_count == 4),
        ("T-04", "Logical AND Compound Filter", "SELECT name, cgpa FROM students WHERE cgpa >= 8.5 AND age > 20;", lambda r: r.returned_count == 4),
        ("T-05", "Logical OR Compound Filter", "SELECT name FROM students WHERE branch = 'MECH' OR branch = 'CIVIL';", lambda r: r.returned_count == 2),
        ("T-06", "Wildcard Projection (*)", "SELECT * FROM students WHERE cgpa >= 9.0;", lambda r: r.returned_count == 2),
        ("T-07", "ORDER BY Ascending Sort", "SELECT name, cgpa FROM students ORDER BY cgpa;", lambda r: r.rows[0]["cgpa"] <= r.rows[-1]["cgpa"]),
        ("T-08", "LIMIT Clause Truncation", "SELECT name FROM students LIMIT 3;", lambda r: r.returned_count == 3),
        ("T-09", "Lexical Error Detection", "SELECT name @ students;", "LexicalError"),
        ("T-10", "Syntax Error (Missing Col)", "SELECT FROM students;", "SyntaxError"),
        ("T-11", "Syntax Error (Missing FROM)", "SELECT name students;", "SyntaxError"),
        ("T-12", "Semantic Error (Unknown Table)", "SELECT name FROM faculty;", "SemanticError"),
        ("T-13", "Semantic Error (Unknown Col)", "SELECT salary FROM students;", "SemanticError"),
        ("T-14", "Semantic Error (Type Mismatch)", "SELECT name FROM students WHERE name > 50;", "SemanticError"),
        ("T-15", "Boundary (Empty Result Set)", "SELECT name FROM students WHERE age > 100;", lambda r: r.returned_count == 0),
        ("T-16", "Pipeline Inspection Stages", "SELECT name, cgpa FROM students WHERE age >= 21;", lambda r: True)
    ]

    print("=" * 80)
    print("      QUERYLANG COMPILER ENGINE - REVIEW 2 VERIFICATION MATRIX")
    print("=" * 80)
    print(f"{'ID':<6} | {'Test Description':<32} | {'Expected Behavior':<25} | {'Status'}")
    print("-" * 80)

    passed = 0
    for tid, desc, q, validator in test_matrix:
        status = "[ FAIL ]"
        try:
            if isinstance(validator, str):
                try:
                    pipeline.execute_query(q)
                except Exception as e:
                    if e.__class__.__name__ == validator:
                        status = "[ PASS ]"
                        passed += 1
            else:
                r = pipeline.execute_query(q)
                if validator(r):
                    status = "[ PASS ]"
                    passed += 1
        except Exception:
            pass
        print(f"{tid:<6} | {desc:<32} | {'Expected ' + str(validator):<25} | {status}")

    print("-" * 80)
    print(f"Total Tests: {len(test_matrix)} | Passed: {passed} | Failed: {len(test_matrix) - passed}")
    print("=" * 80)


def interactive_repl():
    pipeline = CompilerPipeline()
    print("QueryLang Interactive Shell (Type \\quit to exit, \\demo for demo, \\test for tests)")
    buffer = []
    while True:
        try:
            prompt = "QueryLang> " if not buffer else "      ...> "
            line = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not line: continue
        if line == "\\quit": break
        if line == "\\demo": run_demo(); continue
        if line == "\\test": run_tests(); continue
        if line == "\\schema": print(pipeline.catalog.format_catalog()); continue

        buffer.append(line)
        if line.endswith(";"):
            full_query = " ".join(buffer)
            buffer.clear()
            try:
                print(pipeline.execute_query(full_query).format_table())
            except QueryLangError as e:
                print(e.format_diagnostic(full_query))


def main():
    parser = argparse.ArgumentParser(description="QueryLang All-In-One Compiler Driver")
    parser.add_argument("-d", "--demo", action="store_true", help="Run Review 2 demonstrations")
    parser.add_argument("-t", "--test", action="store_true", help="Run verification matrix")
    parser.add_argument("-s", "--schema", action="store_true", help="Display symbol table schema")
    parser.add_argument("-q", "--query", type=str, help="Execute single query")

    args = parser.parse_args()
    if args.demo: run_demo(); return
    if args.test: run_tests(); return
    if args.schema: print(SchemaCatalog().format_catalog()); return
    if args.query:
        p = CompilerPipeline()
        try: print(p.execute_query(args.query).format_table())
        except QueryLangError as e: print(e.format_diagnostic(args.query))
        return

    interactive_repl()


if __name__ == '__main__':
    main()
