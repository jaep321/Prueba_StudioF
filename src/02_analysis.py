import pandas as pd
import os
import io

def run_analysis():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    files = {
        "clientes": "BD_Clientes.xlsx",
        "transaccional": "BD_Transaccional.xlsx"
    }
    
    output = []
    
    for name, filename in files.items():
        path = os.path.join(base_path, filename)
        output.append(f"# Analysis of {filename}")
        try:
            df = pd.read_excel(path)
            output.append(f"- Shape: {df.shape}")
            output.append(f"- Columns: {', '.join(df.columns)}")
            
            # Nulls
            nulls = df.isnull().sum()
            nulls = nulls[nulls > 0]
            if not nulls.empty:
                output.append("- Missing Values:")
                for col, val in nulls.items():
                    output.append(f"  - {col}: {val}")
            else:
                output.append("- No missing values.")
                
            # Sample
            output.append("\n- Sample Data:")
            output.append(df.head(3).to_markdown(index=False))
            
            # Stats (numerical)
            output.append("\n- Numerical Stats:")
            output.append(df.describe().to_markdown())
            
            output.append("\n" + "="*30 + "\n")
            
        except Exception as e:
            output.append(f"Error loading {filename}: {str(e)}")

    with open(os.path.join(base_path, "eda_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    try:
        run_analysis()
        print("Analysis complete. Saved to eda_summary.md")
    except Exception as e:
        print(f"Global Error: {e}")
