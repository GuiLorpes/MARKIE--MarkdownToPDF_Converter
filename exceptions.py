from enum import Enum, auto

exceptions: list[str] = [
"Usage: python md_to_pdf.py --file FILE",
"FILE has a different extension. FILE has to be .md",
"FILE was not found",
"FILE doesn't have contents to convert to PDF"
]

class ExceptionType(Enum):
    '''
    Determines the type of exception that is happening
    '''
    NOARG = auto()
    NOMD = auto()
    DOESNTEXIST = auto()
    ISEMPTY = auto()

class Exceptions:
    '''
    Gives an exeption message in case an error occurs
     - --file is empty
     - *file* doesn't end in .md
     - *file* doesn't exists
     - --file is not empty & *file* exists and ends in .md, but its empty
    '''
    exception: str
    
    def __init__(self, type: ExceptionType):
        match type:
            case ExceptionType.NOARG:
                self.exception = exceptions[0]
            case ExceptionType.NOMD:
                self.exception = exceptions[1]
            case ExceptionType.DOESNTEXIST:
                self.exception = exceptions[2]
            case ExceptionType.ISEMPTY:
                self.exception = exceptions[3]

    def get_exception(self) -> str:
        return self.exception 