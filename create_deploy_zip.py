import zipfile
import os

def create_zip():
    exclude_dirs = {'__pycache__', 'venv', '.git'}
    files_to_include = ['main.py', 'requirements.txt', '.env']
    
    with zipfile.ZipFile('Bit_Bot_Deploy.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add root files
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file}")
        
        # Add cogs directory
        for root, dirs, files in os.walk('cogs'):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path)
                    print(f"Added {file_path}")

if __name__ == "__main__":
    create_zip()
