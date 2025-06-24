"""
HTML Parser Module

Parses HTML content and extracts slide information including text, styling, and layout.
"""

from html.parser import HTMLParser
from typing import Dict, List, Any, Optional
import re


class SlideElement:
    """Represents a single element on a slide"""
    
    def __init__(self, element_type: str, content: str = "", attributes: Dict[str, Any] = None):
        self.type = element_type
        self.content = content
        self.attributes = attributes or {}
        self.children = []
        self.style = {}
        
    def add_child(self, child: 'SlideElement'):
        self.children.append(child)
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'content': self.content,
            'attributes': self.attributes,
            'style': self.style,
            'children': [child.to_dict() for child in self.children]
        }


class SlideHTMLParser(HTMLParser):
    """Parse HTML and extract structured slide content"""
    
    def __init__(self):
        super().__init__()
        self.slides = []
        self.current_slide = None
        self.element_stack = []
        self.current_element = None
        self.in_slide = False
        self.style_context = {}
        
        # Tracking specific elements
        self.in_title = False
        self.in_subtitle = False
        self.in_content = False
        self.current_text = ""
        
        # Slide metadata
        self.title = ""
        self.subtitle = ""
        self.period = ""
        self.logo_text = ""
        
    def parse(self, html_content: str) -> List[Dict[str, Any]]:
        """Parse HTML content and return list of slides"""
        self.feed(html_content)
        return self.get_slides()
        
    def handle_starttag(self, tag: str, attrs: List[tuple]):
        """Handle opening tags"""
        attrs_dict = dict(attrs)
        
        # Check for slide container
        if 'class' in attrs_dict and 'slide-container' in attrs_dict.get('class', ''):
            self.in_slide = True
            self.current_slide = {
                'elements': [],
                'metadata': {},
                'style': self._extract_style(attrs_dict)
            }
            self.slides.append(self.current_slide)
            
        # Track element hierarchy
        if self.in_slide:
            element = SlideElement(tag, attributes=attrs_dict)
            element.style = self._extract_style(attrs_dict)
            
            if self.element_stack:
                self.element_stack[-1].add_child(element)
            else:
                if self.current_slide:
                    self.current_slide['elements'].append(element)
                
            self.element_stack.append(element)
            
            # Special handling for specific elements
            if tag == 'h1':
                self.in_title = True
            elif tag == 'h2':
                self.in_subtitle = True
            elif 'class' in attrs_dict:
                if 'subtitle' in attrs_dict['class']:
                    self.in_content = True
                elif 'logo' in attrs_dict['class']:
                    self.current_element = element
                    
    def handle_endtag(self, tag: str):
        """Handle closing tags"""
        if self.in_slide and self.element_stack and self.element_stack[-1].type == tag:
            element = self.element_stack.pop()
            
            # Store extracted content
            if self.in_title and tag == 'h1':
                self.in_title = False
                self.title = self.current_text.strip()
                element.content = self.title
                self.current_slide['metadata']['title'] = self.title
                self.current_text = ""
                
            elif self.in_subtitle and tag == 'h2':
                self.in_subtitle = False
                self.subtitle = self.current_text.strip()
                element.content = self.subtitle
                self.current_slide['metadata']['subtitle'] = self.subtitle
                self.current_text = ""
                
            elif self.in_content and tag == 'div':
                self.in_content = False
                if '対象期間:' in self.current_text:
                    self.period = self.current_text.split('対象期間:')[1].strip()
                    self.current_slide['metadata']['period'] = self.period
                element.content = self.current_text.strip()
                self.current_text = ""
                
        # End of slide
        if tag == 'div' and self.in_slide and not self.element_stack:
            self.in_slide = False
            self.current_slide = None
                
    def handle_data(self, data: str):
        """Handle text data"""
        if self.in_slide:
            cleaned_data = data.strip()
            if cleaned_data:
                if self.in_title or self.in_subtitle or self.in_content:
                    self.current_text += data
                elif self.element_stack:
                    self.element_stack[-1].content += cleaned_data
                    
    def _extract_style(self, attrs_dict: Dict[str, str]) -> Dict[str, Any]:
        """Extract styling information from attributes"""
        style = {}
        
        # Extract from class names
        if 'class' in attrs_dict:
            classes = attrs_dict['class'].split()
            style['classes'] = classes
            
            # Map Tailwind classes to style properties
            for cls in classes:
                if cls.startswith('text-'):
                    if 'xl' in cls:
                        style['font-size'] = self._map_text_size(cls)
                    elif cls.startswith('text-purple'):
                        style['color'] = '#8a2be2'
                    elif cls.startswith('text-gray'):
                        style['color'] = '#666666'
                elif cls == 'font-bold':
                    style['font-weight'] = 'bold'
                elif cls.startswith('bg-'):
                    style['background-color'] = self._map_bg_color(cls)
                    
        # Extract from style attribute
        if 'style' in attrs_dict:
            style_str = attrs_dict['style']
            style_props = self._parse_style_string(style_str)
            style.update(style_props)
            
        return style
        
    def _map_text_size(self, class_name: str) -> str:
        """Map Tailwind text size classes to point sizes"""
        size_map = {
            'text-5xl': '36pt',
            'text-4xl': '28pt',
            'text-3xl': '24pt',
            'text-2xl': '20pt',
            'text-xl': '18pt',
            'text-lg': '16pt',
            'text-base': '14pt',
            'text-sm': '12pt'
        }
        return size_map.get(class_name, '14pt')
        
    def _map_bg_color(self, class_name: str) -> str:
        """Map Tailwind background classes to colors"""
        color_map = {
            'bg-purple-50': '#f3e8ff',
            'bg-gray-50': '#f9fafb',
            'bg-white': '#ffffff'
        }
        return color_map.get(class_name, '#ffffff')
        
    def _parse_style_string(self, style_str: str) -> Dict[str, str]:
        """Parse inline style string"""
        style_dict = {}
        for prop in style_str.split(';'):
            if ':' in prop:
                key, value = prop.split(':', 1)
                style_dict[key.strip()] = value.strip()
        return style_dict
        
    def get_slides(self) -> List[Dict[str, Any]]:
        """Get parsed slides"""
        return self.slides
        
    def get_metadata(self) -> Dict[str, str]:
        """Get overall document metadata"""
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'period': self.period
        }