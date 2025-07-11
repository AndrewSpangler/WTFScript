prefix = "bs"
requires = ["html"]

def _bs_patch_classes(class_string, patch_classes, reorder=False):
    """Patches bootstrap classes to reuse core html classes"""
    classes = class_string.split(" ")
    for c in reversed(patch_classes):
        if c in classes:
            if reorder:
                classes.remove(c)
            else:
                continue
        classes.insert(0, c)
    return " ".join(classes)

def _bs_patch_div(wtf, patch_classes:list):
    def _patched(content="", classes="", **kw):
        classes = _bs_patch_classes(classes, patch_classes)
        return wtf.div(content=content, classes=classes, **kw)
    return _patched

def _make_patch_dict():
    bs_bp_sizes = ["sm", "md", "lg", "xl", "xxl"]

    simple_divs = [
        "col",
        "row",
        "container",
        "container-fluid",
        "clearfix",
        "accordion",
        "accordion-item",
        "card",
        "card-body",
        "card-header"
    ]

    patched_divs = {
        # "col" : ("div", ("col",)),
    }

    patched_divs.update(
        {
            c.replace("-", "_") : ("div", (c,))
            for c in 
            simple_divs
        }
    )

    for bp in bs_bp_sizes: # add base flexboxes
        patched_divs[f"d_{bp}_flex"] = (("div"), (f"d-{bp}-flex",))
    for bp in bs_bp_sizes: # add inline flexboxes
        patched_divs[f"d_{bp}_inline_flex"] = (("div"), (f"d-{bp}-inline-flex",))

    for t in ("-row", "-col"): # Add flex classes
        for dir  in ("", "-reverse"):
            for bp in ["", *["-"+b for b in bs_bp_sizes]]:
                name = f"flex{t}{bp}{dir}"
                cname = name.replace("-", "_")
                patched_divs[cname] = (("div"), (f"d-flex {name}",))

    for bp in bs_bp_sizes: # add containers
        patched_divs[f"container_{bp}"] = (("div"), (f"container-{bp}",))

    for i in range(6): # add cols
        patched_divs[f"col_{i+1}"] = (("div"), (f"col-{i+1}",))
    for bp in bs_bp_sizes:
        for i in range(12): # add bp cols
            patched_divs[f"col_{bp}_{i+1}"] = (("div"), (f"col-{bp}-{i+1}",))
        patched_divs[f"col_{bp}"] = (("div"), (f"col-{bp}",))

    return patched_divs

def init(wtf):
    binds = {}
    to_patch = _make_patch_dict()
    for k, v in to_patch.items():
        _bs_patch_div
        binds[k] = _bs_patch_div(wtf, v[1])
    return binds