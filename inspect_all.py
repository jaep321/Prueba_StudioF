import zipfile
import xml.etree.ElementTree as ET
import sys

def read_docx(file_path):
    try:
        with zipfile.ZipFile(file_path) as z:
            xml_content = z.read('word/document.xml')
        
        tree = ET.fromstring(xml_content)
        namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        full_text = []
        for p in tree.findall('.//w:p', namespace):
            p_text = []
            for t in p.findall('.//w:t', namespace):
                if t.text:
                    p_text.append(t.text)
            if p_text:
                full_text.append(''.join(p_text))
        
        return '\n'.join(full_text)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI\Prueba_tecnica_clientes.docx"
    print("--- START DOCX CONTENT ---")
    print(read_docx(path))
    print("--- END DOCX CONTENT ---")

    print("\n\n--- CHECKING EXCEL CONTENT ---")
    try:
        import pandas as pd
        excel_files = ["BD_Clientes.xlsx", "BD_Transaccional.xlsx"]
        base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
        
        for f in excel_files:
            file_path = f"{base_path}\\{f}"
            print(f"\nScanning {f}...")
            try:
                # Read first row only to get columns
                df = pd.read_excel(file_path, nrows=0) 
                print(f"Columns in {f}:")
                for col in df.columns:
                    print(f"  - {col}")
            except Exception as e:
                print(f"Could not read {f}: {e}")
                
    except ImportError:
        print("Pandas/Openpyxl not installed.")
    except Exception as e:
        print(f"Error checking excel: {e}")
