import json
import os 

def write_file(path, filename, content):  
    try: 
        print("Writing file", filename) 

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