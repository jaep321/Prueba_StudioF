import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def read_docx(file_path):
    try:
        with zipfile.ZipFile(file_path) as z:
            xml_content = z.read('word/document.xml')
        
        tree = ET.fromstring(xml_content)
        
        # XML namespace for Word
        namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        text = []
        # Find all paragraphs
        for p in tree.findall('.//w:p', namespace):
            p_text = []
            # Find all text runs within paragraph
            for t in p.findall('.//w:t', namespace):
                if t.text:
                    p_text.append(t.text)
            if p_text:
                text.append(''.join(p_text))
        
        return '\n'.join(text)
    except Exception as e:
        return f"Error reading .docx: {str(e)}"

if __name__ == "__main__":
    path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI\Prueba_tecnica_clientes.docx"
    print(read_docx(path))
