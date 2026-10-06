import argparse
from pathlib import Path
from enum import Enum, auto

from exceptions import ExceptionType, Exceptions

from markdown_it import MarkdownIt
from weasyprint import HTML, CSS                                 # type: ignore

CURR_DIR = Path(__file__).resolve().parent
PATH_STYLES: str = f"{CURR_DIR}styles"
STYLES: dict[str, str] = {"base":"base.css", "sbc":"article_sbc.css"}
DARK_STYLE: str = "dark.css"
md = MarkdownIt().enable("table")

error: str
def converter(
        file: str, 
        style: str = "base", 
        dark: bool = False,
        out: str = ""
        ) -> None:
    '''
    Converts *file* into HTML, then into PDF

    If *file* doesn't have any contents, returns an error

    *theme* dictates what theme the PDF will have, light(default) or dark    
    *style* dictates the  the PDF will have

    :type file: str
    :type theme: str
    :type style: str
    :typer: None
    '''
    try:
        with open(file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        error = Exceptions(ExceptionType.DOESNTEXIST).get_exception()
        raise ValueError(f"Error: {error}")

    if content == "" or content.isspace():
        error = Exceptions(ExceptionType.ISEMPTY).get_exception()
        raise ValueError(f"Error: {error}")
    
    body = md.render(content)
    out = file[:-2] + "pdf" if out == "" else out
    css = [CSS(filename=f'{PATH_STYLES}/{STYLES[style]}')]

    if dark:
        css.append(CSS(filename=f'{PATH_STYLES}/dark.css'))

    HTML(string=f''' {body} ''').write_pdf(out, stylesheets=css)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--style", "-s", type=str)
    parser.add_argument("--theme", "-t", action="store_true")
    parser.add_argument("-o", type=str)
    args = parser.parse_args()

    if args.file == "":
        error = Exceptions(ExceptionType.NOARG).get_exception()
        raise ValueError(f"Error: {error}")
    if args.file[-3:] != ".md":
        error = Exceptions(ExceptionType.NOMD).get_exception()
        raise ValueError(f"Error: {error}")

    converter(args.file, args.style ,args.theme, args.o)    


if __name__ == "__main__":
    main()