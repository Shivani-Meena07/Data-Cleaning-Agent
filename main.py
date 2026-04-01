"""
FastAPI entrypoint for the data cleaning application.
This file serves as the standard entrypoint that tools can auto-detect.
"""
from scripts.backend import app

__all__ = ["app"]
