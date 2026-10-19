import argparse
import sys
from pathlib import Path

from exceptions import *

from markdown_it import MarkdownIt
from weasyprint import HTML, CSS             # type: ignore

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from config import LANGS, STYLES, SLIDES_STYLES
from entities import Render, RenderSlides, RenderWithTOC, \
                        ListCSS, SlidesCSS, TocCSS


MODES: dict[str, tuple[type[Render], type[ListCSS]]] = {
    "normal" : (Render, ListCSS),
    "slides" : (RenderSlides, SlidesCSS),
    "toc" : (RenderWithTOC, TocCSS)
}

def get_mode(slides:bool, toc: bool) -> str:
    if slides:
        return "slides"
    if toc:
        return "toc"
    return "normal"


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
            return ""                # unknown/missing language: no contrast
        return highlight(code, lexer, formatter)

    return MarkdownIt("commonmark", {"highlight": highlight_code}).enable("table")


def load_CSS(path: Path) -> CSS:
    ''' Retrieves the CSS file from `path`, if the file doesn't exists raiszes an error '''
    if not path.is_file():
        raise StyleError(f"Style file not found: {path}")

    return CSS(filename=str(path))


def converter(file: str, 
              lang: str,
              slides: bool,
              toc: bool, 
              style: str, 
              dark: bool,
              extras: list[str], 
              target: str
              ) -> None: 
    '''
    Converts `file` into HTML, then into PDF

    If `file` doesn't have any contents, returns an error

    `theme` dictates what theme the PDF will have, light(default) or dark 
    `style` dictates the  the PDF will have

    
    :param file: .md file to be converted    
    :type file: str

    :param lang: Decides what language the HTML will be formated
    :type lang: str

    :param slides: If `True` the PDF will have a slide format
    :type slides: bool

    :param toc: If `True` the PDF will have a table of contents
    :type toc: bool

    :param style: Style that the PDF file is going to be formated into
    :type style: str

    :param dark: Dictates if the PDF has a light or dark theme 
    (False or True, respectively)
    :type dark: bool

    :param extras: List of extra CSS files to edit the original `style`
    :type extras: list[str]

    :param target: Filename where the PDF is going to be written
    :type out: str
    
    :returns out: The PDF, saved in `target` if provided, or in `file` with the 
    .pdf suffix 
    :rtype: None
    '''
    try:
        with open(file, 'r', encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError as e:
        raise InputNotFoundError(f"FILE was not found: {file}") from e

    if content.strip() == "":
        raise EmptyFileError()

    md = make_markdown(dark)

    render_class, css_class = MODES[get_mode(slides, toc)]

    body = render_class(md, content, lang).rendering()
    css = [load_CSS(c) for c in css_class(dark, extras).get_styles(style)]
    
    out = target or str(Path(file).with_suffix(".pdf"))

    HTML(string=f'<html lang="{lang}"><body>{body}</body></html>', \
         base_url=str(Path(file).resolve().parent)). \
            write_pdf(out, stylesheets=css)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str)
    parser.add_argument("--lang", "-l", type=str, default="pt-BR", choices=LANGS)
    parser.add_argument("--slides", action="store_true")
    parser.add_argument("--toc", action="store_true")
    parser.add_argument("--style", "-s", type=str, default="base", choices=STYLES)
    parser.add_argument("--dark", "-d", action="store_true")
    parser.add_argument("--css", "-c", action="append", default=[], metavar="FILE")
    parser.add_argument("-o", type=str, default="")
    args = parser.parse_args()

    try:
        if not args.file:
            raise NoFileError()
        if not args.file.endswith(".md"):
            raise NotMarkdownError()
        if args.slides and args.toc:
            raise OptionConflictError("--slides and --toc can't be used together")

        converter(args.file, args.lang, args.slides, args.toc, args.style ,args.dark, args.css, args.o)    

    except MdToPdfExceptions as e:
        print(f'{e}', file=sys.stderr)
        sys.exit(1)



if __name__ == "__main__":
    main()