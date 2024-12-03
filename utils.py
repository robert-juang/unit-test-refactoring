import json
import os 

#utils.py
def write_file(path, filename, content, type="test"):  
    """
    Given path, filename, and content, write to file

    Ignore file if in IGNORED_FILE defined in constants

    type can be test or refactor
    """
    try: 
        print(f"Writing test for: ", filename) if type == "test" else print(f"Refactoring code for: ", filename)

        with open(path, "w+", encoding="utf-8") as f: 
            f.write(content) 
    except Exception as e: 
        print("Error when writing file with path: ", path) 
        print(e) 
    
def write_json_file(path, content): 
    if not path.endswith(".json"): 
        return None 
    
    filename = os.path.basepath(path) 

    print('Writing, ', filename)

    with open(f"test_{filename}", "w+", encoding="utf-8") as f: 
        json.dump(content) 