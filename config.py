from pathlib import Path


LANGS: dict[str, str] = {"pt-BR":"Conteúdos" , "en-US":"Contents", 
                         "fr" : "Contenus", "es" : "Contenidos"}


CURR_DIR: Path = Path(__file__).resolve().parent


# CSS
PATH_STYLES: Path =  CURR_DIR / "styles"
STYLES: dict[str, Path] = {"base" : PATH_STYLES / "base.css", 
                          "sbc" : PATH_STYLES / "article_sbc.css"}
DARK_STYLE: Path = PATH_STYLES / "dark.css"
TOC_STYLE: Path = PATH_STYLES / "toc.css"
SLIDES_STYLES: dict[str, Path] = {"base" : PATH_STYLES / "base_slides.css"}