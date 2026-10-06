import argparse
import sys
from pathlib import Path

from exceptions import *

from markdown_it import MarkdownIt
from weasyprint import HTML, CSS             # type: ignore

CURR_DIR: Path = Path(__file__).resolve().parent
PATH_STYLES: Path =  CURR_DIR / "styles"
STYLES: dict[str, str] = {"base":"base.css", "sbc":"article_sbc.css"}
DARK_STYLE: str = "dark.css"

md = MarkdownIt().enable("table")
error: str


def converter(file: str, style: str, dark: bool, out: str) -> None:
    '''
    Converts *file* into HTML, then into PDF

    If *file* doesn't have any contents, returns an error

    *theme* dictates what theme the PDF will have, light(default) or dark 
    *style* dictates the  the PDF will have

    :type file: str
    :type theme: str
    :type style: str
    :type dark: bool
    :type out: str
    :typer: None
    '''
    try:
        with open(file, 'r') as f:
            content = f.read()
    except FileNotFoundError as e:
        raise InputNotFoundError(f"FILE was not found: {file}") from e

    if content.strip() == "":
        raise EmptyFileError()
    
    body = md.render(content)
    out = out or str(Path(file).with_suffix(".pdf"))

    if style not in STYLES:
        raise StyleError(
            f"Error: unknown style '{style}'. Options: {', '.join(STYLES)}"
        )

    path = PATH_STYLES / STYLES[style]
    if not path.is_file():
        raise StyleError(f"Error: style file not found: {path}")

    css = [CSS(filename=f'{PATH_STYLES}/{STYLES[style]}')]
    
    if dark:
        css.append(CSS(filename=f'{PATH_STYLES}/{DARK_STYLE}'))

    HTML(string=f''' {body} ''').write_pdf(out, stylesheets=css)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str)
    parser.add_argument("--style", "-s", type=str, default="base")
    parser.add_argument("--theme", "-t", action="store_true")
    parser.add_argument("-o", type=str, default="")
    args = parser.parse_args()

    try:
        if not args.file:
            raise NoFileError()
        if not args.file.endswith(".md"):
            raise NotMarkdownError()

        converter(args.file, args.style ,args.theme, args.o)    

    except MdToPdfExceptions as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()