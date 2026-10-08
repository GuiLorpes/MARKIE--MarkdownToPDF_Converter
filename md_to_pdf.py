import argparse
import sys
from pathlib import Path

from exceptions import *
from render import render_with_toc

from markdown_it import MarkdownIt
from weasyprint import HTML, CSS             # type: ignore

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


CURR_DIR: Path = Path(__file__).resolve().parent
PATH_STYLES: Path =  CURR_DIR / "styles"
STYLES: dict[str, str] = {"base":"base.css", "sbc":"article_sbc.css"}
DARK_STYLE: str = "dark.css"
TOC_STYLE: str = "toc.css"


def make_markdown(dark: bool) -> MarkdownIt:
    formatter = HtmlFormatter(
        nowrap=True,                 
        noclasses=True,              
        style="one-dark" if dark else "igor",
    )

    def highlight_code(code: str, lang: str, attrs: str) -> str:
        try:
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            return ""                # linguagem desconhecida/ausente: sem destaque
        return highlight(code, lexer, formatter)

    return MarkdownIt("commonmark", {"highlight": highlight_code}).enable("table")


def get_CSS(style: str, dark: bool, toc: bool) -> list[CSS]:
    '''
    Search for `style` in `STYLES`, if it exists, get it's path for the CSS

    If `dark` is True, adds it into the CSS list

    If `toc`is True adds it into the CSS list
    '''
    path = PATH_STYLES / STYLES[style]
    if not path.is_file():
        raise StyleError(f"Error: style file not found: {path}")

    css = [CSS(filename=f'{PATH_STYLES}/{STYLES[style]}')]

    if dark:
        css.append(CSS(filename=f'{PATH_STYLES}/{DARK_STYLE}'))

    if toc:
        css.append(CSS(filename=f'{PATH_STYLES}/{TOC_STYLE}'))
    return css


def converter(file: str, toc: bool, style: str, dark: bool, target: str) -> None: 
    '''
    Converts `file` into HTML, then into PDF

    If `file` doesn't have any contents, returns an error

    `theme` dictates what theme the PDF will have, light(default) or dark 
    `style` dictates the  the PDF will have

    
    :param file: .md file to be converted    
    :type file: str
    
    :param style: Style that the PDF file is going to be formated into
    :type style: str

    :param dark: Dictates if the PDF has a light or dark theme 
    (False or True, respectively)
    :type dark: bool

    :param target: Filename where the PDF is going to be written
    :type out: str
    
    :returns out: The PDF, saved in `target` if provided, or in `file` with the 
    .pdf suffix 
    :rtype: None
    '''
    try:
        with open(file, 'r') as f:
            content = f.read()
    except FileNotFoundError as e:
        raise InputNotFoundError(f"FILE was not found: {file}") from e

    if content.strip() == "":
        raise EmptyFileError()

    md = make_markdown(dark)

    if toc:
        body, toc_html = render_with_toc(md, content)
        body = toc_html + body

    else:
        body = md.render(content)    
    
    out = target or str(Path(file).with_suffix(".pdf"))

    css = get_CSS(style, dark, toc)

    HTML(string=f''' {body} ''', base_url=str(Path(file).resolve().parent)).\
        write_pdf(out, stylesheets=css)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str)
    parser.add_argument("--toc", action="store_true")
    parser.add_argument("--style", "-s", type=str, default="base", choices=STYLES)
    parser.add_argument("--dark", "-d", action="store_true")
    parser.add_argument("-o", type=str, default="")
    args = parser.parse_args()

    try:
        if not args.file:
            raise NoFileError()
        if not args.file.endswith(".md"):
            raise NotMarkdownError()

        converter(args.file, args.toc, args.style ,args.dark, args.o)    

    except MdToPdfExceptions as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()