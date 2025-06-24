"""
HTML to PPTX Converter Module

A comprehensive module for converting HTML presentations to PowerPoint (PPTX) format.
"""

__version__ = "1.0.0"
__author__ = "HTML to PPTX Converter"

from .core.converter import HTMLtoPPTXConverter
from .parsers.html_parser import SlideHTMLParser
from .builders.pptx_builder import PPTXBuilder

__all__ = [
    "HTMLtoPPTXConverter",
    "SlideHTMLParser", 
    "PPTXBuilder"
]