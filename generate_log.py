"""Compatibility wrapper so tests can import `generate_log` from project root.
This re-exports `generate_log` from the `lib` package.
"""
from lib.generate_log import generate_log

__all__ = ["generate_log"]
