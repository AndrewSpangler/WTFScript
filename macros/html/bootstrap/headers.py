prefix = "bs"
requires = ["html"]

def _bs_patch_classes(class_string, patch_classes, reorder=False):
    """Patches bootstrap classes to reuse core html classes"""
    classes = class_string.split(" ")
    for c in reversed(patch_classes.split(" ")):
        if c in classes:
            if reorder:
                classes.remove(c)
            else:
                continue
        classes.insert(0, c)
    return " ".join(classes)

def _bs_patch_div(wtf, source_class, patch_classes:str, defaults:dict):
    def _patched(content="", classes="", **kw):
        _defaults = defaults.copy()
        _defaults.update(kw)
        if patch_classes:
            classes = _bs_patch_classes(classes, patch_classes)
        # Fetch filter from wtf object by name
        filter_callback = getattr(wtf, source_class)
        return filter_callback(content=content, classes=classes, **_defaults)
    return _patched
   

def _make_patch_dict():
    bs_bp_sizes = ["sm", "md", "lg", "xl", "xxl"]
    colors = [
        "primary", "secondary", "success", "danger",
        "warning", "info", "light", "dark", "link"
    ]

    simple_divs = [
        "accordion", "accordion-item", "accordion-body", "alert", "col", "row",
        "container", "container-fluid", "clearfix", "card", "card-body", "card-header",
        "card-footer", "d-grid", "input-group"
    ]

    patched_classes = {
        "accordion-button": ("button", "accordion-button", {}),
        "alert": ("div", "alert", {"role": "alert"}),
        "alert-link": ("a", "alert-link", {}),
        "alert-heading": ("h4", "alert-heading", {}),
        "abtn": ("a", "btn", {}),
        "btn": ("button", "btn", {}),
        "btn-close": ("button", "btn-close", {}),
        "btn-close-disabled": ("button", "btn-close", {"disabled": True}),
        "btn-close-dark": ("button", "btn-close", {"data-bs-theme": "Dark"}),
        "btn-close-dark-disabled": ("button", "btn-close", {"data-bs-theme": "Dark", "disabled": True}),
        "btn-group": ("div", "btn-group", {"role": "group"}),
        "btn-toolbar": ("div", "btn-toolbar", {"role": "toolbar"}),
        "badge": ("span", "badge", {}),
        "breadcrumb-nav": ("nav", None, {"aria-label": "breadcrumb"}),
        "breadcrumb-ol": ("ol", "breadcrumb", {}),
        "breadcrumb-ul": ("ul", "breadcrumb", {}),
        "breadcrumb-item": ("li", "breadcrumb-item", {}),
        "blockquote": ("blockquote", "blockquote", {}),
        "card-text": ("p", "card-text", {}),
        "card-title": ("h5", "card-title", {}),
        "card-subtitle": ("h6", "card-subtitle", {}),
        "list-group": ("ul", "list-group", {}),
        "list-group-numbered": ("ol", "list-group-numbered", {}),
        "list-group-flush": ("ul", "list-group list-group-flush", {}),
        "list-group-item": ("li", "list-group-item", {}),
        "list-group-item-action": ("li", "list-group-item list-group-item-action", {}),
        "list-group-horizontal": ("ul", "list-group list-group-horizontal", {}),
        "carousel": ("div", "carousel", {}),
        "carousel-dark": ("div", "carousel", {"data-bs-theme": "dark"}),
        "carousel-inner": ("div", "carousel-inner", {}),
        "carousel-item": ("div", "carousel-item", {}),
        "carousel-caption": ("div", "carousel-caption", {}),
        "carousel-control-prev": ("button", "carousel-control-prev", {"type": "button", "data-bs-slide": "prev"}),
        "carousel-control-prev-icon": ("span", "carousel-control-prev-icon", {}),
        "carousel-control-next": ("button", "carousel-control-next", {"type": "button", "data-bs-slide": "next"}),
        "carousel-control-next-icon": ("span", "carousel-control-next-icon", {}),
        "carousel-indicators": ("div", "carousel-indicators", {}),
        "collapse": ("div", "collapse", {}),
        "collapse-horizontal": ("div", "collapse collapse-horizontal", {}),
        "collapse-multi": ("div", "collapse multi-collapse", {}),
        "dropdown": ("div", "dropdown", {}),
        "dropdown-center": ("div", "dropdown-center", {}),
        "dropdown-menu": ("ul", "dropdown-menu", {}),
        "dropdown-menu-end": ("ul", "dropdown-menu dropdown-menu-end", {}),
        "dropdown-menu-dark": ("ul", "dropdown-menu", {"data-bs-theme": "Dark"}),
        "dropdown-button": ("button", "btn dropdown-toggle", {"type": "button", "data-bs-toggle": "dropdown", "aria-expanded": False}),
        "dropdown-a-button": ("a", "btn dropdown-toggle", {"role": "button", "data-bs-toggle": "dropdown", "aria-expanded": False}),
        "dropdown-item": ("button", "dropdown-item", {"type": "button"}),
        "dropdown-item-active": ("button", "dropdown-item active", {"type": "button", "aria-current": "true"}),
        "dropdown-item-disabled": ("button", "dropdown-item disabled", {"type": "button", "aria-current": "true"}),
        "dropdown-item-a": ("a", "dropdown-item", {}),
        "dropdown-item-a-active": ("a", "dropdown-item active", {"aria-current": "true"}),
        "dropdown-item-a-disabled": ("a", "dropdown-item disabled", {"aria-current": "true"}),
        "dropdown-header": ("h6", "dropdown-header", {}),
        "dropdown-toggle": ("button", "btn dropdown-toggle", {"type": "button", "data-bs-toggle": "dropdown"}),
        "dropup": ("div", "btn-group dropup", {}),
        "dropup-center": ("div", "dropup-center dropup", {}),
        "dropend": ("div", "btn-group dropend", {}),
        "dropstart": ("div", "btn-group dropstart", {}),
        "modal": ("div", "modal", {}),
        "modal-dialog": ("div", "modal-dialog", {}),
        "modal-dialog-scrollable": ("div", "modal-dialog modal-dialog-scrollable", {}),
        "modal-dialog-centered": ("div", "modal-dialog modal-dialog-centered", {}),
        "modal-dialog-centered-scrollable": ("div", "modal-dialog modal-dialog-centered modal-dialog-scrollable", {}),
        "modal-content": ("div", "modal-content", {}),
        "modal-header": ("div", "modal-header", {}),
        "modal-title": ("h5", "modal-title", {}),
        "modal-body": ("div", "modal-body", {}),
        "modal-footer": ("div", "modal-footer", {}),
        "nav-item": ("li", "nav-item", {}),
        "nav-link": ("a", "nav-link", {}),
        "nav-link-active": ("a", "nav-link active", {}),
        "nav-link-disabled": ("a", "nav-link disabled", {}),
        "navbar": ("nav", "navbar", {}),
        "navbar-dark": ("nav", "navbar navbar-dark", {}),
        "navbar-light": ("nav", "navbar navbar-light", {}),
        "navbar-expand": ("nav", "navbar-expand", {}),
        "navbar-brand": ("a", "navbar-brand", {}),
        "navbar-toggler": ("button", "navbar-toggler", {"type": "button", "data-bs-toggle": "collapse"}),
        "navbar-toggler-icon": ("span", "navbar-toggler-icon", {}),
        "navbar-collapse": ("div", "collapse navbar-collapse", {}),
        "rounded-pill-badge": ("span", "badge rounded-pill", {}),
        "offcanvas-body": ("div", "offcanvas-body", {}),
        "offcanvas-title": ("h5", "offcanvas-title", {}),
        "pagination": ("ul", "pagination", {}),
        "pagination-center": ("ul", "pagination justify-content-center", {}),
        "page-item": ("li", "page-item", {}),
        "page-item-active": ("li", "page-item active", {}),
        "page-item-disabled": ("li", "page-item active", {}),
        "page-link": ("a", "page-link", {}),
        "span-placeholder": ("span", "placeholder", {}),
        "progress": ("div", "progress", {"role":"progressbar"}),
        "progress_bar": ("div", "progress-bar", {}),
        "progress_stacked": ("div", "progress-stacked", {}),
    }

    # Add simple divs with underscore keys
    patched_classes.update({
        c.replace("-", "_"): ("div", c, {}) for c in simple_divs
    })

    # Add nav and nav-ul
    nav_variants = [
        ("", ""), ("-fill", "nav-fill"), ("-underline", "nav-underline"),
        ("-underline-center", "nav-underline justify-content-center"),
        ("-underline-fill", "nav-underline nav-fill"),
        ("-pills", "nav-pills"), ("-pills-center", "nav-pills justify-content-center"),
        ("-pills-fill", "nav-pills nav-fill"), ("-tabs", "nav-tabs"),
        ("-tabs-center", "nav-tabs justify-content-center"),
        ("-tabs-fill", "nav-tabs nav-fill"), ("-center", "justify-content-center"),
        ("-vertical", "flex-column"), ("-end", "justify-content-end")
    ]

    for suffix, cls in nav_variants:
        base_class = f"nav {cls}".strip()

        for state in ["", "active", "disabled"]:
            key_suffix = f"-{state}" if state else ""
            for direction in ["", "vertical"]:
                dir_suffix = f"-{direction}" if direction else ""
                state_class = " nav-link"
                if state: state_class += " "+state
                if direction: state_class += " flex-column"
                patched_classes[f"nav-ul{suffix}{key_suffix}{dir_suffix}"] = ("ul", base_class+state_class, {})
                patched_classes[f"nav{suffix}{key_suffix}{dir_suffix}"] = ("nav", base_class+state_class, {})

    for siz in bs_bp_sizes:
        _siz = "-"+siz if siz else "" 
        for start in ("", "start", "end", "top", "bottom"):
            for show in ("", "show"):
                class_string = "offcanvas"
                name_string = ""
                if start:
                    class_string += " offcanvas-"+start 
                    name_string += "-"+start
                if show:
                    class_string + " "+"show"
                    name_string += "-show"

                patched_classes[f"offcanvas{_siz}{name_string}"] = ("ul", class_string, {})
                patched_classes[f"offcanvas{_siz}-dark{name_string}"] = ("ul", class_string, {"data-bs-theme":"dark"})
                patched_classes[f"offcanvas{_siz}-light{name_string}"] = ("ul", class_string, {"data-bs-theme":"light"})
      

    # Add buttons, progress bars, badges, and list group variants per color
    for color in colors:
        for style_prefix, style_class in [("", ""), ("outline_", "outline-")]:
            cls_suffix = f"{style_class}{color}"
            for size in ["sm", "lg"]:
                size_class = f"btn btn-{cls_suffix} btn-{size}"
                patched_classes[f"btn_{style_prefix}{color}_{size}"] = ("button", size_class, {})
                patched_classes[f"btn_{style_prefix}{color}_{size}_disabled"] = (
                    "button", size_class, {"disabled": True}
                )
                a_class = f"btn btn-{cls_suffix} btn-{size}"
                patched_classes[f"a_btn_{style_prefix}{color}_{size}"] = ("a", a_class, {})
                patched_classes[f"a_btn_{style_prefix}{color}_{size}_disabled"] = (
                    "a", a_class, {
                        "aria-disabled": "true", "tabindex": "-1",
                        "role": "button", "class": f"{a_class} disabled"
                    }
                )

        # Progress bars
        patched_classes[f"progress_bar_{color}"] = ("div", f"progress-bar bg-{color}", {})
        patched_classes[f"progress_bar_{color}_striped"] = ("div", f"progress-bar bg-{color} progress-bar-striped", {})
        patched_classes[f"progress_bar_{color}_animated"] = (
            "div", f"progress-bar bg-{color} progress-bar-striped progress-bar-animated", {}
        )

    # Badges (rounded pills)
    patched_classes[f"rounded_pill_badge_{color}"] = ("span", f"badge text-bg-{color} rounded-pill", {})


    # Responsive button and group classes
    for bp in bs_bp_sizes[:3]:
        patched_classes[f"btn_{bp}"] = ("button", f"btn-{bp}", {})
        patched_classes[f"btn_group_{bp}"] = ("div", f"btn-group-{bp}", {"role": "group"})

    # Responsive containers, list groups, flex
    for bp in bs_bp_sizes:
        patched_classes[f"d_{bp}_flex"] = ("div", f"d-{bp}-flex", {})
        patched_classes[f"d_{bp}_inline_flex"] = ("div", f"d-{bp}-inline-flex", {})
        patched_classes[f"container_{bp}"] = ("div", f"container-{bp}", {})
        patched_classes[f"list_group_horizontal_{bp}"] = ("div", f"list-group list-group-horizontal-{bp}", {})
        patched_classes[f"navbar_expand_{bp}"] = ("div", f"navbar navbar-expand-{bp}", {})

    # Flex row/col (and reverse)
    for t in ("-row", "-col"):
        for direction in ("", "-reverse"):
            for bp in [""] + [f"-{b}" for b in bs_bp_sizes]:
                cname = f"flex{t}{bp}{direction}".replace("-", "_")
                patched_classes[cname] = ("div", f"d-flex flex{t}{bp}{direction}", {})

    # Grid columns
    for i in range(1, 13):
        patched_classes[f"col_{i}"] = ("div", f"col-{i}", {})
        for bp in bs_bp_sizes:
            patched_classes[f"col_{bp}_{i}"] = ("div", f"col-{bp}-{i}", {})
        patched_classes[f"col_{bp}"] = ("div", f"col-{bp}", {})

    # Sanitize dashes
    for k, v in patched_classes.copy().items():
        if not "-" in k:
            continue
        patched_classes[k.replace("-", "_")] = patched_classes.pop(k)

    return patched_classes

def init(wtf):
    binds = {}
    to_patch = _make_patch_dict()
    for k, v in to_patch.items():
        source, patch, defaults = v
        binds[k] = _bs_patch_div(wtf, source, patch, defaults)
    return binds

if __name__ == "__main__":
    import json
    data = _make_patch_dict()
    print("\n\n", json.dumps(sorted(data.keys()), indent=2))
    print("\n\n", len(data))