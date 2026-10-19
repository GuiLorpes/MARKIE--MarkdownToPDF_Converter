from config import STYLES, SLIDES_STYLES, DARK_STYLE, TOC_STYLE, Path
from render import render_with_toc, render_slides
from exceptions import StyleError

from markdown_it import MarkdownIt


# Rendering Classes

class Render:
    def __init__(self, md: MarkdownIt, content: str, lang: str):
        self.md, self.content, self.lang = md, content, lang
    def rendering(self) -> str:
        return self.md.render(self.content)

class RenderWithTOC(Render):
    def rendering(self) -> str:
        body, toc = render_with_toc(self.md, self.content, self.lang)
        return toc + body

class RenderSlides(Render):
    def rendering(self) -> str:
        return render_slides(self.md, self.content)  


# CSS List Classes

class ListCSS:
    ''' Base class to get the CSS styles '''
    styles: dict[str, Path] = STYLES
    modes_styles: tuple[Path, ...] = ()

    def __init__(self, dark: bool, extras: list[str]):
        self.dark = dark
        self.extras = [Path(e) for e in extras]

    def get_styles(self, style: str) -> list[Path]:
        paths = []
        if style not in self.styles:
            raise StyleError(\
                f"Unknown style '{style}'. Options: {', '.join(self.styles)}")
        paths.append(self.styles[style])

        if self.dark: 
            paths.append(DARK_STYLE)

        paths += self.modes_styles
        paths += self.extras

        return paths

class SlidesCSS(ListCSS):
    styles: dict[str, Path] = SLIDES_STYLES

class TocCSS(ListCSS):
    modes_styles: tuple[Path, ...] = (TOC_STYLE,)
