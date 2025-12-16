import zipfile
import os
import pandas as pd

def extract_xml_and_scan_excel():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    docx_path = os.path.join(base_path, "Prueba_tecnica_clientes.docx")
    
    # Extract document.xml
    try:
        with zipfile.ZipFile(docx_path) as z:
            with open(os.path.join(base_path, "document.xml"), "wb") as f:
                f.write(z.read("word/document.xml"))
        print("Extracted document.xml")
    except Exception as e:
        print(f"Error extracting XML: {e}")

    # Scan Excel
    excel_files = ["BD_Clientes.xlsx", "BD_Transaccional.xlsx"]
    for f in excel_files:
        file_path = os.path.join(base_path, f)
        print(f"\n--- Columns in {f} ---")
        try:
            df = pd.read_excel(file_path, nrows=0)
            for col in df.columns:
                print(col)
        except Exception as e:
            print(f"Error reading {f}: {e}")

if __name__ == "__main__":
    extract_xml_and_scan_excel()
