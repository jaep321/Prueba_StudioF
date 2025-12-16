import os
import shutil

def setup_project_structure():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    
    # Define directories
    dirs = ['src', 'input', 'output', 'images']
    for d in dirs:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)
        print(f"Created: {d}")
        
    # Move Files
    # Map: (Source, Destination Folder, New Name)
    moves = [
        ("step1_eda.py", "src", "01_eda.py"),
        ("step2_analysis.py", "src", "02_analysis.py"),
        ("step3_segmentation.py", "src", "03_segmentation.py"),
        ("step3a_check_values.py", "src", "utils_check_values.py"),
        ("step3b_recency.py", "src", "utils_check_recency.py"),
        ("Clientes_Segmentados.csv", "output", "Clientes_Segmentados.csv"),
        ("Entrega_Prueba.md", "output", "Reporte_Tecnico.md") # Rename for clarity
    ]
    
    # Also move input files if not already there (Optional, maybe copy?)
    # Users usually prefer inputs to stay where they found them or be moved.
    # The user said "as if I were to upload to git". Inputs usually aren't in git if large.
    # I'll leave inputs in root or move them? The request implies "samples" of data.
    # I'll move the excel files to input/ for cleanliness, but warn if they are open.
    
    for src_name, dst_folder, dst_name in moves:
        src = os.path.join(base_path, src_name)
        dst = os.path.join(base_path, dst_folder, dst_name)
        
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"Moved: {src_name} -> {dst_folder}/{dst_name}")
            except Exception as e:
                print(f"Error moving {src_name}: {e}")
        else:
            print(f"Skipped (not found): {src_name}")

if __name__ == "__main__":
    setup_project_structure()
