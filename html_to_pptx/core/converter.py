"""
Main Converter Module

Orchestrates the HTML to PPTX conversion process.
"""

import os
from typing import Optional
from ..parsers.html_parser import SlideHTMLParser
from ..builders.pptx_builder import PPTXBuilder


class HTMLtoPPTXConverter:
    """Main converter class for HTML to PPTX conversion"""
    
    def __init__(self, use_native: bool = False):
        """
        Initialize the converter
        
        Args:
            use_native: Force native XML generation even if python-pptx is available
        """
        self.parser = SlideHTMLParser()
        self.builder = PPTXBuilder(use_native=use_native)
        
    def convert(self, html_input: str, output_path: str, is_file: bool = True) -> bool:
        """
        Convert HTML to PPTX
        
        Args:
            html_input: Path to HTML file or HTML content string
            output_path: Path to save the PPTX file
            is_file: Whether html_input is a file path (True) or content string (False)
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Get HTML content
            if is_file:
                if not os.path.exists(html_input):
                    raise FileNotFoundError(f"HTML file not found: {html_input}")
                with open(html_input, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            else:
                html_content = html_input
                
            # Parse HTML
            slides = self.parser.parse(html_content)
            metadata = self.parser.get_metadata()
            
            # Build PPTX
            self.builder.build(slides, output_path, metadata)
            
            print(f"Successfully created: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error during conversion: {str(e)}")
            return False
            
    def convert_file(self, html_file: str, output_file: Optional[str] = None) -> bool:
        """
        Convert HTML file to PPTX
        
        Args:
            html_file: Path to HTML file
            output_file: Optional output file path (defaults to replacing .html with .pptx)
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        if output_file is None:
            output_file = os.path.splitext(html_file)[0] + '.pptx'
            
        return self.convert(html_file, output_file, is_file=True)
        
    def convert_string(self, html_content: str, output_file: str) -> bool:
        """
        Convert HTML string to PPTX
        
        Args:
            html_content: HTML content as string
            output_file: Output file path
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        return self.convert(html_content, output_file, is_file=False)