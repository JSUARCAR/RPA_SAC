
import configparser
import sys
import os

# Add current dir to path to find core
sys.path.append(os.getcwd())

from core.data_handler import DataHandler

def debug_main():
    print("DEBUG: Starting debug_launcher")
    
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'Paths' not in config:
            print("ERROR: 'Paths' section missing in config.ini")
            return
            
        print("DEBUG: Config loaded. Paths section present.")
        print(f"DEBUG: Source path: {config['Paths'].get('source_excel_path')}")
        print(f"DEBUG: Dest dir: {config['Paths'].get('dest_dir')}")

        print("DEBUG: Initializing DataHandler...")
        data_handler = DataHandler(config['Paths'])
        print("DEBUG: DataHandler initialized.")
        
        print("DEBUG: Calling get_pending_tasks...")
        tasks = data_handler.get_pending_tasks()
        print(f"DEBUG: Tasks found: {len(tasks)}")
        
        for t in tasks:
            print(f"Task: {t}")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_main()
