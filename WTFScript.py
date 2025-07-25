import datetime
import importlib
import inspect
import json
import os
import traceback
from jinja2 import Environment, BaseLoader
from typing import Callable, Iterable
from lxml import etree, html

PYTHON_BINDS = {
    all,
    any,
    bin,
    bool,
    bytearray,
    bytes,
    dict,
    dir,
    divmod,
    enumerate,
    filter,
    float,
    getattr,
    hasattr,
    hex,
    int,
    isinstance,
    issubclass,
    len,
    list, 
    max,
    min,
    next,
    oct,
    pow,
    range,
    reversed,
    round,
    set,
    slice,
    sorted,
    str,
    sum,        
    tuple,
    type,
    zip
}

def accumulate(iterable:Iterable, callback:Callable, *args, **kw) -> list[str]:
    """
    Applies a callback function to each item in the iterable and returns
    the results as a list
    """
    return [callback(i, *args, **kw) for i in iterable]
def acc(*args, **kw): return accumulate(*args, **kw)

def join_accumulate(iterable:Iterable, callback:Callable, join_string="", *args, **kw) -> str:
    """
    Applies a callback function to each item in the iterable,
    joins the results with a string
    """
    return join_string.join(accumulate(iterable, callback, *args, **kw))
def jacc(*args, **kw): return join_accumulate(*args, **kw)   

def collect_attribute(itterable:Iterable, attr:str) -> list:
    """
    Collects a list of attributes from an itterable and returns the results
    as a list.
    """
    return [getattr(i, attr) for i in itterable]
def cattr(*args, **kw): return collect_attribute(*args, **kw)   

def join_collect_attribute(itterable:Iterable, attr:str, join_string="") -> str:
    """
    Collects a list of attributes from an itterable,
    joins the results with a string
    """
    return join_string.join([str(getattr(i, attr)) for i in itterable])
def jcattr(*args, **kw): return join_collect_attribute(*args, **kw)   

def cull(itterable:Iterable, strip=True) -> list[object]:
    """
    Removes null / empty values from a list
    By default strips whitespace from strings
    """
    return [
        x 
        for x in itterable 
        if ( 
            (
                (x.strip() if strip else x)
                if (x.strip() if strip else x)
                else False
            )
            if isinstance(x, str) else
            (x if x else False)
        )
    ]
def jcull(itterable:Iterable, join_string="") -> str:
    """
    Cull list and join the results with a string
    """
    return join_string.join(cull(itterable))

def capitalize(s:str) -> str:
    return s.capitalize()

def step_accumulate(iterable: Iterable, callback: Callable, step=1, *args, **kw) -> list[list[object]]:
    """
    Returns accumulated values as list of accumulations of size <= step.
    If the number of items is not evenly divisible by step, the final group
    will contain the remainder, returns the results as a list of lists.

    Example:
    def mult_2(v):
        return 2 * v
    res = step_accumulate([1,2,3], mult_2, step=2)
    res => [[2,4], [6]]
    """
    it = iter(iterable)
    result = []
    while True:
        batch = list()
        try:
            for _ in range(step):
                batch.append(next(it))
        except StopIteration:
            pass
        if not batch:
            break
        result.append(accumulate(batch, callback, *args, **kw))
    return result
def sacc(*args, **kw): return step_accumulate(*args, **kw)   


def flatten_structure(data: Iterable, level: int = 0) -> list[tuple[int, str]]:
    """
    Recursively flattens nested iterables into a list of (indent_level, item) tuples.
    Treats strings and bytes as atomic (non-iterable).
    
    Example:
    ["Item A", ["Subitem A1", "Subitem A2"], "Item B"]
    -> [(0, "Item A"), (1, "Subitem A1"), (1, "Subitem A2"), (0, "Item B")]
    """
    flattened = []
    for item in data:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            flattened.extend(flatten_structure(item, level + 1))
        else:
            flattened.append((level, str(item)))
    return flattened
def flas(*args, **kw): return flatten_structure(*args, **kw)   


def format_bytes(size:int) -> str:
    """Nicely formats a byte count"""
    for suffix in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if size < 1024: break
        size /= 1024
    return "{:.2f} {}".format(size, suffix)


def format_seconds(time_in_seconds:int)->str:
    """
    Formats an integer number of seconds to a nice H:MM:SS format
    """
    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    out = ""
    if int(hours): out += f"{int(hours)}:"
    if int(hours) or int(minutes): out += f"{str(int(minutes)).zfill(2)}:"
    return out + f"{str(int(seconds)).zfill(2)}"


def from_timestamp(time_in:int)->datetime.datetime:
    """
    Helper function to convert Unix timestamp to datetime object
    """
    return datetime.datetime.fromtimestamp(time_in)


def from_rfc_timestamp(ts:str) -> datetime.datetime:
    """Common with Docker, Kubernetes, etc"""
    ts_trimmed = ts[:26]
    return datetime.datetime.strptime(ts[:26], "%Y-%m-%dT%H:%M:%S.%f")


def pretty_from_timestamp(time_in:int, *args, **kw)->str:
    return pretty_date(from_timestamp(time_in), *args, **kw)


def localize(utc_datetime:datetime.datetime) -> datetime.datetime:
    """Localize to system timezone"""
    if not utc_datetime: return None
    return utc_datetime.replace(tzinfo=datetime.timezone.utc).astimezone()


def get_tz_from_localization(local_tz) -> str:
    """Template helper function to get server's local tz"""
    return (
        datetime.datetime.now()
        .replace(tzinfo=datetime.timezone.utc)
        .astimezone(local_tz)
    ).strftime("%Z")


def pretty_date(
        local_datetime: datetime.datetime,
        seconds: bool = False,
        minutes: bool = True,
        hours: bool = True,
        use24: bool=True,
        show_tz: bool=False
    ) -> str:
    """
    Helper function to make dates look better
    """
    if not local_datetime: return None
    format_string = f"%m/%d/%y "
    if hours: format_string += f"%{'H' if use24 else 'I'}"
    if minutes: format_string += ":%M"
    if seconds: format_string += ":%S"
    if not use24: format_string += "%p"
    if show_tz: format_string += "%Z"
    t = local_datetime.strftime(format_string)
    return t


class RenderException(Exception):
     def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class TemplateRenderer:
    def __init__(self, name, template_str: str, env: Environment):
        self.name = name
        self.env = env
        try:
            self.template = self.env.from_string(template_str)
        except Exception as e:
            print(traceback.print_exc())
            raise RenderException(f"Error loading template from string - {template_str}")

    def render(self, **kw) -> str:
        try:
            return self.template.render(**kw)
        except Exception as e:
            try:
                data = json.dumps(kw, indent=2)
            except:
                try:
                    data = str(kw)
                except:
                    data = "Not serializable"
            
            print(f"Error rendering - {self.name} with arguments - {data}")
            raise e
            
class ModuleNamespace:
    def __init__(self):
        pass

class WTFScript:
    reserved = [
        "app", # For future Flask environment (or other app) injection feature 
        "env", # Prevent overwrite
        "loaded_filters", # Preven overwrite
        "macros", # Prevent overwrite
        "render", # Renders wtf script string
        "renderers", # Prevent overwrite
        "reserved", # This
        "signatures", # Prevent overwrite
        "load_macros_dir", # Prevent overwrite
    ]

    # Core binds that handle iteration in WTFScript
    # Without these, itteration is very hard.
    # Also includes formatting tools for dates and bytes
    wtf_binds = {
        # Base accumulate itterator
        acc, accumulate,
        # Base collect attribute itterator
        cattr, collect_attribute,
        # Base accumulate-join itterator
        jacc, join_accumulate,
        # Base collect-join itterator
        jcattr, join_collect_attribute,
        # Step-wise accumulate itterator
        sacc, step_accumulate,
        # Structure flattener for lists operator macros
        flas, flatten_structure,
        # Culling to remove empty values from lists
        cull, jcull,
        # Capitalize function for accumulators
        capitalize,
        # Pretty-print byte counts
        format_bytes,
        # Unix timestamp -> datetime
        from_timestamp,
        # RFC timestamp -> datetime
        from_rfc_timestamp,
        # Seconds -> hh:mm:ss
        format_seconds,
        # Pretty-print date
        pretty_date,
        # Pretty date from timestamp
        pretty_from_timestamp,
        # Localize datetime object
        localize,
        # Get local timezone string
        get_tz_from_localization
    }

    # Core python binds
    # This allows most core python to be used in WTFScript
    python_binds = PYTHON_BINDS

    def __init__(
        self,
        binds:dict = {}, # Map of { names : callables} to register
        macro_dirs = [], # list of macro folder paths
    ):
        self.macros = {}
        self.renderers = {}
        self.signatures = {}
        self.dummy_functions = {}
        self.loaded_filters = {}
        self.module_namespaces = {}

        # Create shared Jinja2 environment
        self.env = Environment(loader=BaseLoader())

        # WTF core functions
        for builtin in self.wtf_binds:
            self._bind(builtin.__name__, builtin)
        
        # Built-in Python functions
        for builtin in self.python_binds:
            self._bind(builtin.__name__, builtin)

        # External
        for name, callback in binds.items():
            self._bind(name, callback)
        
        for path in macro_dirs:
            self.load_macros_dir(path)
    
    def load_macros_dir(self, macros_dir:os.PathLike) -> list[str]:
        """Load dummy functions from headers.py"""
        prefix, dummy_functions = self._load_headers_file(macros_dir)
        self.dummy_functions.update(dummy_functions)
        loaded = []
        macros_dir = os.path.join(macros_dir, "templates")
        if os.path.exists(macros_dir):
            for ent in os.scandir(macros_dir):
                if ent.name.endswith(".template"):
                    _name = ent.name[:-9]
                    name = (prefix+"." if prefix else "")+_name
                    
                    with open(ent.path) as f:
                        template = f.read()
                    self.macros[name] = template
                    func = self.dummy_functions.get(name)
                    
                    sig = inspect.signature(func) if func else None
                    try:
                        renderer = TemplateRenderer(name, template, env=self.env)
                    except Exception as e:
                        print(f'Error loading renderer for - "{name}" - {e}')
                        raise e
                    self.renderers[name] = renderer
                    self.signatures[name] = sig
                    filt = self._make_filter(name)
                    self._bind(name, filt)
                    loaded.append(name)
        print(f"Loaded ", len(loaded), " filters")
        return loaded
        
    def _bind(self, name: str, callback: Callable) -> None:
        """
        Bind callable as a Jinja2 global and filter.
        Supports dotted names like 'bs.button'.
        """
        if name.startswith("_"):
            raise ValueError(
                f"Cannot bind macro {name} - macros starting with underscores are not allowed by WTFScript"
            )
        if name in self.reserved:
            raise ValueError(f"Cannot bind macro {name} - name is reserved.")

        # Always register full dotted name for filter/global access
        self.env.filters[name] = callback
        self.env.globals[name] = callback

        # Create attribute access for dot notation
        if "." in name:
            namespace_name, attr_name = name.split(".", 1)

            # Create namespace if it doesn't exist
            if not hasattr(self, namespace_name):
                ns = ModuleNamespace()
                setattr(self, namespace_name, ns)
                self.env.globals[namespace_name] = ns
                self.env.filters[namespace_name] = ns
            else:
                ns = getattr(self, namespace_name)

            # Set the function as an attribute of the namespace
            setattr(ns, attr_name, callback)

        else:
            # Flat attribute
            setattr(self, name, callback)


    def _load_headers_file(self, path: os.PathLike) -> dict:
        """Load dummy functions for arg checking and bind helpers."""
        header_path = os.path.join(path, "headers.py")
        spec = importlib.util.spec_from_file_location("header", header_path)
        header_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(header_module)

        prefix = getattr(header_module, "prefix", "")
        if prefix:
            print(f"Creating namespace with prefix - {prefix}")
            ns = ModuleNamespace()
            setattr(self, prefix, ns)
            self.env.filters[prefix] = ns
            self.env.globals[prefix] = ns

        init = getattr(header_module, "init", None)
        if init:
            print(f"Initializing extension at {path}")
            binds = init(self)
            print(f"Found {len(binds)} binds")

            new_binds = {(prefix+"."+k):v for k,v in binds.items()}
            # print("New Binds:", json.dumps(list(i for i in new_binds.keys())))
            for k, v in new_binds.items():
                self._bind(k, v)

            print(f"Loaded {len(binds)} binds")

        all_funcs = {
            (prefix+"." if prefix else "")+name: func
            for name, func in inspect.getmembers(header_module, inspect.isfunction)
            if not name.startswith("_")
        }

        helpers = getattr(header_module, "helpers", [])
        for func in helpers:
            if callable(func):
                self._bind(func.__name__, func)
                all_funcs.pop(func.__name__)

        aliases = getattr(header_module, "aliases", [])
        for func in aliases:
            if callable(func):
                name = func.__name__
                parent_name = func()
                filt = self._make_alias(name, parent_name)
                self._bind(name, filt)
                all_funcs.pop(name)

        return prefix, all_funcs

    def _make_alias(self, _name, parent_name):
        def _render_alias(*args, **kwargs):
            return self._render_macro(parent_name, *args, **kwargs)
        return _render_alias
        

    def _make_filter(self, _name):
        def _render_filter(*args, **kwargs):
            return self._render_macro(_name, *args, **kwargs)
        return _render_filter

    def _render_macro(self, _name, *args, **kwargs):
        """
        Renders a macro after confirming argument signature from headers.py
        """ 
        name = _name
        renderer = self.renderers.get(name)
        sig = self.signatures.get(name)

        if not renderer or not sig:
            raise ValueError(f"No macro named '{name}' or missing signature")

        try:
            # Check if the signature has **kwargs
            has_var_keyword = any(
                param.kind == param.VAR_KEYWORD
                for param
                in sig.parameters.values()
            )
            
            if has_var_keyword:
                # If function accepts **kwargs,
                # Bind and pass the rest as kwargs
                bound = sig.bind_partial(*args, **kwargs)
                bound.apply_defaults()
                context = dict(bound.arguments)
                # Bind unbound
                bound_param_names = set(bound.arguments.keys())
                sig_param_names = set(sig.parameters.keys())
                # Find unspecified args
                extra_kwargs = {
                    k: v
                    for k, v in kwargs.items()
                    if k not in sig_param_names
                }
                # Bundle as kw
                if extra_kwargs:
                    context['kw'] = extra_kwargs
                else:
                    context['kw'] = {}
            else:
                bound = sig.bind_partial(*args, **kwargs)
                bound.apply_defaults()
                context = dict(bound.arguments)
                
        except TypeError as e:
            raise ValueError(f"Invalid arguments for macro '{name}': {e}")
        
        try:
            return renderer.render(**context)
        except Exception as e:
            raise ValueError(f"Error rendering macro '{name}': {e}")
        

    def render(self, content: str, *args, **kw) -> str:
        template = self.env.from_string(content)
        return template.render(*args, **kw)

    def render_template(self, path:os.PathLike, *args, **kw) -> str:
        with open(path, "r") as f:
            content=f.read()
        return self.render(content, *args, **kw)
    
    
class WTFHtml(WTFScript):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.load_macros_dir(os.path.join(os.path.dirname(__file__), "macros/html/core"))

    def render(self, content: str, *args, **kw) -> str:
        content = super().render(content, *args, **kw)
        # document_root = html.fromstring(content)
        # content = etree.tostring(document_root, encoding='unicode', pretty_print=True)
        return content

class WTFHtmlFlask(WTFHtml):
    def __init__(self, app, *args, **kw):
        self.app = app
        super().__init__(*args, **kw)
        self.load_macros_dir(os.path.join(os.path.dirname(__file__), "macros/html/core"))

    def _bind(self, name: str, callback: Callable) -> None:
        super()._bind(name, callback)

        self.app.jinja_env.filters[name] = callback
        self.app.jinja_env.globals[name] = callback

        if "." in name:
            namespace_name, _ = name.split(".", 1)
            ns = getattr(self, namespace_name, None)
            if ns:
                self.app.jinja_env.filters[namespace_name] = ns
                self.app.jinja_env.globals[namespace_name] = ns

    def render(self, content: str, *args, **kw) -> str:
        return super().render(content, *args, **kw)

    @property
    def jinja_env(self):
        return self.env


class WTFMd(WTFScript):
    def __init__(self, *args, **kw):
        WTFScript.__init__(self, *args, **kw)
        self.load_macros_dir(os.path.join(os.path.dirname(__file__), "macros/markdown/core"))


if __name__ == "__main__":
    py_script = """
if __name__ == "__main__":
    wtf = WTFScript()
    macros_dir = os.path.join(os.path.dirname(__file__), "macros/markdown/core")
    wtf.load_macros_dir(macros_dir)

    wd = os.path.dirname(__file__)
    with open(os.path.join(wd, "README.wtf"), "r") as f:
        wtf_script=f.read()
    
    with open(os.path.join(wd, "example.html.wtf"), "r") as f:
        html_script=f.read()

    rendered = wtf.render(
        wtf_script,
        wtf_script=wtf_script,
        py_script=py_script,
        html_script=html_script
    )
    with open(os.path.join(wd, "README.md"), "w+") as f:
        f.write(rendered)
    """
    wtf = WTFScript()
    macros_dir = os.path.join(os.path.dirname(__file__), "macros/markdown/core")
    wtf.load_macros_dir(macros_dir)

    wd = os.path.dirname(__file__)
    with open(os.path.join(wd, "examples/README.wtf"), "r") as f:
        wtf_script=f.read()
    
    with open(os.path.join(wd, "examples/example.html.wtf"), "r") as f:
        html_script=f.read()

    rendered = wtf.render(
        wtf_script,
        wtf_script=wtf_script,
        py_script=py_script,
        html_script=html_script
    )
    with open(os.path.join(wd, "README.md"), "w+") as f:
        f.write(rendered)