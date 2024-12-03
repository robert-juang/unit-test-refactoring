class DirectoryNodeInitError(Exception): 
    code = 400 
    description = "Failure to initialize direcotry node"

class DirectoryNodeNotExistError(Exception): 
    code = 400 
    description = "Directory Node does"

class FileNodeInitError(Exception): 
    code = 400 
    description = "Failure to initialize file node"

class DirectoryGenerationError(Exception): 
    code = 400 
    description = "Error when generation directory"

class UnitTestGenerationError(Exception): 
    code = 400 
    description = "Error when generating unit test" 

class RefactorGenerationError(Exception): 
    code = 400 
    description = "Error when generating refactoring code"