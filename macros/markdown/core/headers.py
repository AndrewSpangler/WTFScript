"""Lays out arg config for macros, all args must be keywords. Defaults may be set here."""

def blockquote(content=""): pass
def bold(content=""): pass
def br(content=""): pass
def bolditalic(content=""): pass
def center(content=""): pass
def code(content=""): pass
def codeblock(content=""): pass
def escape(content=""): pass
def header1(content=""): pass
def header2(content=""): pass
def header3(content=""): pass
def header4(content=""): pass
def header5(content=""): pass
def header6(content=""): pass
def hr(content=""): pass
def image(content="", href="", title=""): pass
def italic(content=""): pass
def link(content="", href="", title=""): pass
def listitem(content=""): pass
def orderedlist(content=""): pass
def paragraph(content=""): pass
def unorderedlist(content=""): pass
def url(content="", href="", title=""): pass
# Aliases
def a(*args, **kw):
    """Alias for link"""
    return "link"
def b(*args, **kw):
    """Alias for bold"""
    return "bold"
def bi(*args, **kw):
    """Alias for bolditalic"""
    return "bolditalic"
def c(*args, **kw):
    """Alias for code"""
    return "code"
def cb(*args, **kw):
    """Alias for codeblock"""
    return "codeblock"
def e(*args, **kw):
    """Alias for url"""
    return "url"
def email(*args, **kw):
    """Alias for url"""
    return "url"
def em(*args, **kw):
    """Alias for bold"""
    return "bold"
def h1(*args, **kw):
    """Alias for header1"""
    return "header1"
def h2(*args, **kw):
    """Alias for header2"""
    return "header2"
def h3(*args, **kw):
    """Alias for header3"""
    return "header3"
def h4(*args, **kw):
    """Alias for header4"""
    return "header4"
def h5(*args, **kw):
    """Alias for header5"""
    return "header5"
def h6(*args, **kw):
    """Alias for header6"""
    return "header6"
def i(*args, **kw):
    """Alias for italic"""
    return "italic"
def img(*args, **kw):
    """Alias for image"""
    return "image"
def li(*args, **kw):
    """Alias for listitem"""
    return "listitem"
def ol(*args, **kw):
    """Alias for orderedlist"""
    return "orderedlist"
def p(*args, **kw):
    """Alias for paragraph"""
    return "paragraph"
def ul(*args, **kw):
    """Alias for unorderedlist"""
    return "unorderedlist"
aliases = [a, b, bi, c, cb, e, email, em, h1, h2, h3, h4, h5, h6, i, img, li, ol, p, ul]