class MdToPdfExceptions(Exception):
    ''' 
    Base class for all exceptions raised by this project
    Subclasses define a default message, which can be overridden
    to add details (e.g. the file name).
    '''
    default_message = "Unexpected error"

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class NoFileError(MdToPdfExceptions):
    '''Raised when no file is passed as argument'''
    default_message = (
        "Usage: \n"
        "python md_to_pdf.py --file [-f] FILE \n"
        "    --slides\n"
        "    --toc\n"
        "    --style [-s] STYLE\n"
        "    --dark [-d]\n"
        "    --css EXTRA_STYLES\n"
        "    -o OUT.pdf\n"
    )


class NotMarkdownError(MdToPdfExceptions):
    '''Raised when FILE doesn't have the .md extension'''
    default_message = "FILE has a different extension. FILE has to be .md"


class InputNotFoundError(MdToPdfExceptions):
    '''Raised when FILE doesn't exist'''
    default_message = "FILE was not found"


class EmptyFileError(MdToPdfExceptions):
    '''Raised when FILE exists but has nothing to convert'''
    default_message = "FILE doesn't have contents to convert to PDF"


class StyleError(MdToPdfExceptions):
    '''Raised when the chosen style (or its .css file) can't be used'''
    default_message = "Invalid style"

class OptionConflictError(MdToPdfExceptions):
    '''Raised when two options can't be used together'''
    default_message = "These options can't be used together"