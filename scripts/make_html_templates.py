import os

base_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
output_path = os.path.join(base_folder, "macros/html/core/templates")
os.makedirs(output_path, exist_ok=True)

header_py_path = os.path.join(base_folder, "macros/html/core/headers.py")
header_lines = ['"""Lays out arg config for macros, all args must be keywords. Defaults may be set here."""\n']

tags = {
    "a":["href","hreflang","media","ping","referrerpolicy","rel","target","type"],
    "abbr":[],
    "address":[],
    "area":["alt","coords","download","hreflang","media","referrerpolicy","rel","shape","target","type"],
    "article":[],
    "aside":[],
    "audio":["src", "preload"],
    "b": [],
    "base": ["href", "target"],
    "bdi": [],
    "bdo": [],
    "blockquote": ["cite"],
    "body": [],
    "br": [],
    "button": ["autofocus", "disabled", "form", "formaction", "formenctype", "formmethod", "formnovalidate", "formtarget", "popovertarget", "popovertargetaction", "name", "type", "value"],
    "canvas": ["height", "width"],
    "caption": [],
    "cite": [],
    "code": [],
    "col": ["span"],
    "colgroup": ["span"],
    "data": ["value"],
    "datalist": [],
    "dd": [],
    "del": ["cite", "datetime"],
    "details": ["open"],
    "dfn": [],
    "dialog": ["open"],
    "div": [],
    "dl": [],
    "dt": [],
    "em": [],
    "embed": ["height", "src", "type", "width"],
    "fieldset": ["disabled", "form", "name"],
    "figcaption": [],
    "figure": [],
    "footer": [],
    "form": ["accept-charset", "action", "autocomplete", "enctype", "method", "name", "novalidate", "rel", "target"],
    "h1": [],
    "h2": [],
    "h3": [],
    "h4": [],
    "h5": [],
    "h6": [],
    "head": [],
    "header": [],
    "hgroup": [],
    "hr": [],
    "html": ["xmlns"],
    "i": [],
    "iframe": ["allow", "allowfullscreen", "allowpaymentrequest", "height", "loading", "name", "referrerpolicy", "sandbox", "src", "srcdoc", "width"],
    "img": ["alt", "crossorigin", "height", "ismap", "loading", "longdesc", "referrerpolicy", "sizes", "src", "srcset", "usemap", "width"],
    "input": ["accept", "alt", "autocomplete", "autofocus", "checked", "dirname", "disabled", "form", "formaction", "formenctype", "formmethod", "formnovalidate", "formtarget", "height", "list", "max", "maxlength", "min", "minlength", "multiple", "name", "pattern", "placeholder", "popovertarget", "popovertargetaction", "readonly", "required", "size", "src", "step", "type", "value", "width"],
    "ins": ["cite", "datetime"],
    "kbd": [],
    "label": ["for", "form"],
    "legend": [],
    "li": ["value"],
    "link": ["crossorigin", "href", "hreflang", "media", "referrerpolicy", "rel", "sizes", "type"],
    "main": [],
    "map": ["name"],
    "mark": [],
    "menu": [],
    "meta": ["charset", "content", "http_equiv", "name"],
    "meter": ["form", "high", "low", "max", "min", "optimum", "value"],
    "nav": [],
    "noscript": [],
    "object": ["data", "form", "height", "name", "type", "typemustmatch", "usemap", "width"],
    "ol": ["reversed", "start", "type"],
    "optgroup": ["disabled", "label"],
    "option": ["disabled", "label", "selected", "value"],
    "output": ["for", "form", "name"],
    "p": [],
    "param": ["name", "value"],
    "picture": [],
    "pre": [],
    "progress": ["max", "value"],
    "q": ["cite"],
    "rp": [],
    "rt": [],
    "ruby": [],
    "s": [],
    "samp": [],
    "script": ["async", "crossorigin", "defer", "integrity", "nomodule", "referrerpolicy", "src", "type"],
    "search": [],
    "section": [],
    "select": ["autofocus", "disabled", "form", "multiple", "name", "required", "size"],
    "small": [],
    "source": ["media", "sizes", "src", "srcset", "type"],
    "span": [],
    "strong": [],
    "style": ["media", "type"],
    "sub": [],
    "summary": [],
    "sup": [],
    "svg": [],
    "table": [],
    "tbody": [],
    "td": ["colspan", "headers", "rowspan"],
    "template": [],
    "textarea": ["autofocus", "cols", "dirname", "disabled", "form", "maxlength", "name", "placeholder", "readonly", "required", "rows", "wrap"],
    "tfoot": [],
    "th": ["abbr", "colspan", "headers", "rowspan", "scope"],
    "thead": [],
    "time": ["datetime"],
    "title": [],
    "tr": [],
    "track": ["default", "kind", "label", "src", "srclang"],
    "u": [],
    "ul": [],
    "var": [],
    "video": [],
    "wbr": [],
    "comment": [],
    "doctype": []
}


attr_rename = {
    "for": "for_",
    "async": "async_"
}

rename = {
    "del" : "del_",
    "map" : "map_",
    "object": "object_"
}

global_attributes = [
    "accesskey", "contenteditable", "dir", "draggable", "enterkeyhint", "hidden",
    "inert", "inputmode", "lang", "popover", "spellcheck", "style", "tabindex",
    "title", "translate"
]

not_has_global_attributes = [
    "doctype"
]

not_has_content = [
    "area", "br", "hr", "input", "link", "param", "source", "track", "doctype"
]

common_bool_fields = {
    "autofocus", "checked", "disabled", "readonly", "required", "selected",
    "hidden", "multiple", "novalidate", "formnovalidate", "default", "open",
    "autoplay", "controls", "loop", "muted", "ismap", "nomodule", "reversed",
    "typemustmatch", "allowfullscreen", "itemscope", "inert"
}

tag_bool_fields = {
    "audio": ["controls", "autoplay", "loop", "muted"],
    "button": ["autofocus", "disabled", "formnovalidate"],
    "details": ["open"],
    "dialog": ["open"],
    "fieldset": ["disabled"],
    "form": ["novalidate"],
    "iframe": ["allowfullscreen", "allowpaymentrequest"],
    "img": ["ismap"],
    "input": ["autofocus", "checked", "disabled", "formnovalidate", "multiple", "readonly", "required"],
    "menuitem": ["default"],
    "ol": ["reversed"],
    "optgroup": ["disabled"],
    "option": ["disabled", "selected"],
    "script": ["async", "defer", "nomodule"],
    "select": ["autofocus", "disabled", "multiple", "required"],
    "textarea": ["autofocus", "disabled", "readonly", "required"],
    "track": ["default"],
    "video": ["autoplay", "controls", "loop", "muted"],
}




def html_attr_to_py_name(attr):
    if attr in attr_rename:
        return attr_rename[attr]
    return attr.replace('-', '_')


def py_name_to_html_attr(py_name):
    for html_name, py_name_mapped in attr_rename.items():
        if py_name == py_name_mapped:
            return html_name
    return py_name.replace('_', '-')


def val_field_template(attr, html_attr=None):
    if html_attr is None:
        html_attr = attr
    return '{% if ' + attr + ' %}' + html_attr + '="{{ ' + attr + ' | safe }}" {% endif %}'


def bool_field_template(attr, html_attr=None):
    if html_attr is None:
        html_attr = attr
    return '{% if ' + attr + ' %}' + html_attr + ' {% endif %}'


def construct_field_snippet(tag: str, fields: list[str]) -> str:
    parts = []

    bool_fields = set(tag_bool_fields.get(tag, [])) | (common_bool_fields & set(fields))
    val_fields = [f for f in fields if f not in bool_fields]

    if "classes" in val_fields:
        parts.append('{% if classes %}class="{{ classes | safe }}" {% endif %}')
        val_fields.remove("classes")

    if "id" in val_fields:
        parts.append(val_field_template("id"))
        val_fields.remove("id")

    for f in sorted(val_fields):
        html_attr = py_name_to_html_attr(f)
        parts.append(val_field_template(f, html_attr))

    for f in sorted(bool_fields):
        html_attr = py_name_to_html_attr(f)
        parts.append(bool_field_template(f, html_attr))

    parts.append('{% for key, value in attrs.items() %}{% if value is not none %}{{ key.replace("_", "-") }}="{{ value | safe }}" {% endif %}{% endfor %}')

    return "".join(parts)


def construct_template(tag: str, fields: list[str]) -> str:
    if tag == "doctype":
        return "<!DOCTYPE html>"
    elif tag == "comment":
        return "<!-- {{ content }} -->"

    has_content = tag not in not_has_content
    attr_string = construct_field_snippet(tag, fields).strip()

    if attr_string:
        tag_open = f"<{tag} {attr_string}>"
    else:
        tag_open = f"<{tag}>"

    tags_need_closing = {"script", "style"}

    if has_content or tag in tags_need_closing:
        return f"{tag_open}{{{{ content | safe }}}}</{tag}>"
    else:
        return tag_open


def construct_header_signature(tag: str, fields: list[str]) -> str:
    if tag == "doctype":
        return "def doctype(): pass"
    if tag == "comment":
        return "def comment(content=\"\"): pass"

    args = []

    if tag not in not_has_content:
        args.append('content=""')
    if "classes" in fields:
        args.append('classes=""')
    if "id" in fields:
        args.append('id=""')

    extras = [f for f in fields if f not in {"content", "classes", "id"}]
    for arg in sorted(extras):
        args.append(f'{arg}=""')

    args.append('**attrs')

    func_name = rename.get(tag, tag)
    args_str = ", ".join(args)
    return f"def {func_name}({args_str}): pass"


for tag, tag_specific_fields in tags.items():
    print(f"Processing tag: {tag}")
    fields = []

    if tag not in not_has_global_attributes:
        fields += ["id", "classes"] + global_attributes
    fields += tag_specific_fields
    
    fields = [html_attr_to_py_name(field) for field in fields]

    template_str = construct_template(tag, fields)
    template_filename = rename.get(tag, tag) + ".template"
    file_path = os.path.join(output_path, template_filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template_str + "\n")

    header_lines.append(construct_header_signature(tag, fields))


with open(header_py_path, "w", encoding="utf-8") as f:
    file = "\n".join(header_lines)
    file += """\n
prefix = ""
requires=[]
    """
    print(f"Writing - {file}")
    f.write(file)