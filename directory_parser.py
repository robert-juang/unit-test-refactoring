import logging 
import os 
from utils import * 
from errors import * 
from helper import * 

class FileNode: 
    def __init__(self, path: str):
        if (not os.path.isfile(path)): 
            raise FileExistsError
        self.type: str = "file" 
        self.path: str = path 
        self.name: str = os.path.basename(path) 
        self.unit_test_path: str = self._get_unit_test_path(self.path, self.name) 
        self.size: str = "" #TODO: use module to get 
        self.file_content_modified: str = ""
        self.past_file_content: list[str] = [] #tracks past version of unit test in case we want to revert (maybe use dict bc i think we should only use 5 so we don't have ridiculous memory)

        try: 
            with open(path, "r") as f: 
                self.file_content_original: str = f.read() 
        except Exception as e: 
            logging.error("Error when reading file: ",e) 
            self.file_content_original = ""

    def _get_unit_test_path(current_path, file_name): 
        # TODO Figure this shit out 
        intermediate_path = "" #TODO: subtract the path below from current_path 
        return os.path.join("/Users/zhidongjiang/Desktop/unit-test-refactoring", intermediate_path, f"test_{file_name}")

    def unit_test(self): 
        """ Run unit test in the file. Return the unit tested code"""
        pass 

    def refactor(self): 
        """Refactor the code in this file. Return the refactored code"""


class DirectoryNode: 
    def __init__(self, path: str):
        if (not os.path.isdir(path)): 
            raise DirectoryNodeInitError
        self.type: str = "dir"
        self.path: str = path 
        self.name: str = os.path.basename(path)
        self.directory_content: list[FileNode | DirectoryNode] = []

class DirectoryTree: 
    """
    Representing a folder using a tree structure 
    """
    def __init__(self, 
                 root_path: str): 
        self.root = self.recursive_generate(DirectoryNode(root_path)) 

        #TODO: maybe add a cache here for fast retrieval for projects with tons of files 

    def recursive_generate(self, dir_node: DirectoryNode): 
        """ 
        Recursively populate the directory node

        If file append 

        If directory recurse and populate 
        """ 
        if (not os.path.isdir(dir_node.path)): 
            raise DirectoryGenerationError

        for node in list(os.listdir(dir_node.path)): 
            path_to_node: str = os.path.join(dir_node.path, node)

            if os.path.isfile(path_to_node): 
                dir_node.directory_content.append(FileNode(path_to_node))
                 
            if os.path.isdir(path_to_node):
                directory_node = DirectoryNode(path_to_node)
                directory_content = self.recursive_generate(directory_node)
                dir_node.directory_content.append(directory_content)

        return dir_node
        
class DirectoryParser: 
    def __init__(self, root_path: str): 
        self.directory_tree: DirectoryTree = DirectoryTree(root_path)
        #TODO: get size of directory tree and save that
    
    #TODO: make this into a decorator
    def _crawl_directory(self, 
                         dir_node: DirectoryNode, 
                         file_func, 
                         dir_func, 
                         dir_level: int = 0): 
        """crawl through all file and print out file or dir name
        
        Must include file_func and dir_func in case of what to do when encountering different file types
        """
        if (not os.path.isdir(dir_node.path)): 
            raise DirectoryGenerationError
    
        for node in dir_node.directory_content: 
            path_to_node: str = os.path.join(dir_node.path, node.name)
            
            if os.path.isdir(path_to_node):
                dir_func(dir_level, node) 
                dir_level += 1
                self._crawl_directory(dir_node=node, 
                                      file_func=file_func, 
                                      dir_func=dir_func, 
                                      dir_level=dir_level)
                dir_level -= 1

            if os.path.isfile(path_to_node): #function 2
                file_func(dir_level, node)
                 
    def display_tree(self): 
        """scan through entire tree and display a structure to view"""
        print(self.directory_tree.root.name, "(root)")

        self._crawl_directory(self.directory_tree.root, 
                file_func=lambda dir_level, node: print('\t' * dir_level, '|', node.name),  
                dir_func=lambda dir_level, node: print("\t" * dir_level + "- ", node.name), 
        ) 
    
    def retrieve_information(self, node): 
        """Return information about the node"""

        if (node.type == "dir"): 
            return {
                "type": node.type,
                "filename": node.name, 
                "path": node.path, 
                "directory_content": node.directory_content
            }
        elif (node.type == "file"): 
            return {
                "type": node.type,
                "filename": node.name, 
                "path": node.path,
                "content": node.file_content_original, 
                "unit_test": self.file_content_modified, 
                "past_unit_test_versions": self.past_file_content
            }

    def _retrieve_file(self, dir_node, file_name): 
        """Scan through the entire tree and if filename match return node of file otherwise return None
        
        TODO: Maybe can optimize with a faster tree ?? Also add error cehcking

        """

        for node in dir_node.directory_content: 
            path_to_node: str = os.path.join(dir_node.path, node.name)
            
            if os.path.isdir(path_to_node):
                n = self._retrieve_file(node, file_name=file_name)
                if n: 
                    return n
            if os.path.isfile(path_to_node) and os.path.basename(path_to_node) == file_name: 
                return node 
            
        return None 
    
    def retrieve_node_by_filename(self, file_name): 
        """Scan thorugh the entire tree and return matching node by file name. If duplicate, raise error"""
        result = self._retrieve_file(self.directory_tree.root, file_name)
        
        return result if result else None 
    
    def _generate_and_write_files(self, 
                            root: DirectoryNode, 
                            ignore_items: list[str]): 
        """
        Generate and write test files for root. Use file_content_original for the test
        """
        if not root: 
            raise DirectoryNodeNotExistError

        for node in root.directory_content: 
            print("Processing, ", node.name) 
            path_to_node: str = os.path.join(root.path, node.name)

            if os.path.isdir(path_to_node):
                self._write_folder_all(node, ignore_items)

            if os.path.isfile(path_to_node): 
                os.makedirs(node.unit_test_path, exist_ok=True)

                write_file(node.unit_test_path, 
                           node.name,
                           node.file_content_original) 
                
    #TODO: get different versions to populate shit 
