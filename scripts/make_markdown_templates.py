import os
from typing import Iterable

base_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
output_path = os.path.join(base_folder, "macros/markdown/core/templates")
os.makedirs(output_path, exist_ok=True)

header_py_path = os.path.join(base_folder, "macros/markdown/core/headers.py")
header_lines = ['"""Lays out arg config for macros, all args must be keywords. Defaults may be set here."""\n']

aliases = {
    "a"  : "link",
    "b"  : "bold",
    "bi" : "bolditalic",
    "c"  : "code",
    "cb" : "codeblock",
    "e"  : "url",
    "email" : "url",
    "em" : "bold",
    "h1" : "header1",
    "h2" : "header2",
    "h3" : "header3",
    "h4" : "header4",
    "h5" : "header5",
    "h6" : "header6",
    "i"  : "italic",
    "img": "image",
    "li" : "listitem",
    "ol" : "orderedlist",
    "p"  : "paragraph",
    "ul" : "unorderedlist",
}

alias_names = ", ".join(aliases.keys())

tags = {
    "blockquote": ["content"],
    "bold": ["content"],
    "br": ["content"],
    "bolditalic": ["content"],
    "center": ["content"],
    "code": ["content"],
    "codeblock": ["content"],
    "escape": ["content"],
    "header1": ["content"],
    "header2": ["content"],
    "header3": ["content"],
    "header4": ["content"],
    "header5": ["content"],
    "header6": ["content"],
    "hr": ["content"],
    "image": ["content", "href", "title"],
    "italic": ["content"],
    "link": ["content", "href", "title"],
    "listitem": ["content"],
    "orderedlist": ["content"],     # expects list of tuples: (level, item)
    "paragraph": ["content"],
    "unorderedlist": ["content"],   # expects list of tuples: (level, item)
    "url": ["content", "href", "title"]
}

formats = {
    "blockquote": "> {{ content|safe }}",
    "bold": "**{{ content|safe }}**",
    "bolditalic": "***{{ content|safe }}***",
    "br": "{{ content|safe }}  \n",
    "code": "`{{ content|safe }}`",
    "codeblock": "      {{ content|safe }}",
    "center": "<center>{{ content|safe }}</center>",
    "escape": "{{ content }}",
    "header1": "# {{ content|safe }}\n",
    "header2": "## {{ content|safe }}\n",
    "header3": "### {{ content|safe }}\n",
    "header4": "#### {{ content|safe }}\n",
    "header5": "##### {{ content|safe }}\n",
    "header6": "###### {{ content|safe }}\n",
    "hr": "{{ content|safe }}\n\n---\n\n",
    "image": "![{{ content|safe }}]({{ href|safe }}{{ (' "' + title + '"' ) if title else '' }})",
    "italic": "*{{ content|safe }}*",
    "link": "[{{ content|safe }}]({{ href|safe }}{{ (' "' + title + '"' ) if title else '' }})",
    "listitem": "- {{ content|safe }}\n",
    "orderedlist" : """
{% set counters = [0] * 10 %}
{% for level, item in flatten_structure(content) %}
{% set _ = counters.__setitem__(level, counters[level] + 1) %}
{% for i in range(level + 1, 10) %}{% set _ = counters.__setitem__(i, 0) %}{% endfor %}
{{ '  ' * level }}{{ counters[level] }}. {{ item }}
{% endfor %}""".strip(),
    "paragraph": "{{ content|safe }}",
    "unorderedlist": "{% for level, item in flatten_structure(content) %}{{ '  ' * level }}- {{ item }}\n{% endfor %}\n",
    "url": "<{{ href|safe }}>",
}


def construct_alias(name:str, parent:str) -> str:
    return f'def {name}(*args, **kw):\n    """Alias for {parent}"""\n    return "{parent}"'

def construct_header_signature(tag: str, fields: list[str]) -> str:
    args = [f'{f}=""' for f in fields]
    args_str = ", ".join(args)
    return f"def {tag}({args_str}): pass"


for tag, fields in tags.items():
    print(f"Processing tag: {tag}")
    template_str = formats[tag]
    template_filename = tag + ".template"
    file_path = os.path.join(output_path, template_filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template_str + "\n")
    header_lines.append(construct_header_signature(tag, fields))

aliases = "\n".join([construct_alias(a,p) for a, p in aliases.items()])
aliases += f"\naliases = [{alias_names}]"

file = "\n".join(header_lines)
file += "\n" + "# Aliases\n" + aliases

with open(header_py_path, "w", encoding="utf-8") as f:
    f.write(file)