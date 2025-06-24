#!/usr/bin/env python3
"""
Command Line Interface for HTML to PPTX Converter

Usage:
    python -m html_to_pptx.cli input.html [output.pptx] [--native]
"""

import sys
import argparse
from .core.converter import HTMLtoPPTXConverter


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Convert HTML presentations to PowerPoint (PPTX) format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python -m html_to_pptx.cli input.html
  python -m html_to_pptx.cli input.html output.pptx
  python -m html_to_pptx.cli input.html --native
        '''
    )
    
    parser.add_argument(
        'input',
        help='Input HTML file path'
    )
    
    parser.add_argument(
        'output',
        nargs='?',
        help='Output PPTX file path (optional, defaults to input name with .pptx extension)'
    )
    
    parser.add_argument(
        '--native',
        action='store_true',
        help='Use native XML generation instead of python-pptx library'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Create converter
    converter = HTMLtoPPTXConverter(use_native=args.native)
    
    # Convert file
    success = converter.convert_file(args.input, args.output)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()