from dataclasses import dataclass

import re
from html import escape

from markdown_it import MarkdownIt
from markdown_it.token import Token


def slugify(s: str) -> str:
    '''
    Transforms `s` lowering every letter, removing every symbol and changing 
    spaces into hyphens

    Examples
    >>> slugify("Abcdé the rest 0L4$")
    'abcdé-the-rest-0l4'
    '''
    slug = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", slug)


def heading_text(inline: Token) -> str:
    ''' Gets the text of the `inline` title without the use of bold text '''
    return "".join(
        t.content for t in (inline.children or [])
        if t.type in ("text", "code_inline")
    )


def render_with_toc(
        md: MarkdownIt, 
        content: str, 
        max_level: int = 3
    ) -> tuple[str, str]:
    '''  '''
    tokens = md.parse(content)
    entries: list[tuple[int, str, str]] = []
    used: dict[str, int] = {}

    for i, tok in enumerate(tokens):
        if tok.type != "heading_open":
            continue
        level = int(tok.tag[1])
        if level > max_level:
            continue

        text = heading_text(tokens[i + 1])
        slug = slugify(text) or "section"
        n = used.get(slug, 0)
        used[slug] = n + 1
        if n:
            slug = f"{slug}-{n}"

        tok.attrSet("id", slug)
        entries.append((level, text, slug))

    body = md.renderer.render(tokens, md.options, {})

    return body, build_toc(entries)


def build_toc(entries: list[tuple[int, str, str]]) -> str:
    '''  '''
    if not entries:
        return ""

    itens = "\n".join(
        f'<li class="level-{lvl}"><a href="#{slug}">{escape(text)}</a></li>'
        for lvl, text, slug in entries
    )
    return f'<nav class="toc"><div class="toc-title">Contents</div><ul>\n{itens}\n</ul></nav>'