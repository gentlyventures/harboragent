#!/usr/bin/env python3
"""
Extract text content from DOCX file and save as structured markdown
"""
import zipfile
import xml.etree.ElementTree as ET
import re
import sys

def extract_text_from_docx(docx_path):
    """Extract all text content from a DOCX file"""
    z = zipfile.ZipFile(docx_path)
    doc = z.read('word/document.xml')
    root = ET.fromstring(doc)
    
    # Define namespace
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    # Extract all text elements
    texts = []
    for t in root.findall('.//w:t', ns):
        if t.text:
            texts.append(t.text)
        elif t.tail:
            texts.append(t.tail)
    
    full_text = ''.join(texts)
    
    # Clean up: remove excessive whitespace but preserve structure
    full_text = re.sub(r'\n{3,}', '\n\n', full_text)
    full_text = re.sub(r' {2,}', ' ', full_text)
    
    return full_text

if __name__ == '__main__':
    docx_path = sys.argv[1] if len(sys.argv) > 1 else 'private_source/paid-pack-v1.0-unprocessed.docx'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'private_source/extracted_content.txt'
    
    content = extract_text_from_docx(docx_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Extracted {len(content)} characters to {output_path}")

