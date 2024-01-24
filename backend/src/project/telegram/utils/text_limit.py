from functools import lru_cache
from typing import Literal

from bs4 import BeautifulSoup
from lxml import html

ALLOWED_TAGS = {
    'b',
    'strong',
    'i',
    'em',
    'u',
    'ins',
    's',
    'strike',
    'del',
    'tg-spoiler',
    'a',
    'tg-emoji',
    'code',
    'pre',
}


@lru_cache()
def shrink_text(text: str, limit: Literal[4096] | Literal[1024]) -> str:
    if not text:
        return text

    suffix = ''
    if len(text) > limit:
        limit -= 3
        suffix = '...'

    broken_html = text[:limit]

    # Use lxml to fix broken html
    parser = html.HTMLParser(remove_blank_text=True)
    root = html.fromstring(broken_html, parser=parser)
    fixed_html = html.tostring(root, method='xml', encoding='unicode')

    # Use BeautifulSoup to unwrap disallowed tags
    soup = BeautifulSoup(fixed_html, 'lxml')

    for tag in soup.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()

    return str(soup) + suffix
