# WTFScript
## Web Template Format Script Engine
WTFScript is a Jinja2-based macro rendering engine for building structured content using custom-defined filters and aliases. Macros are stored as .template files with arguments specified via dummy functions for argument validation.

## Features
- Macro-based rendering using Jinja2 filters
- A simple system to create your own 'cores' for custom languages, or theming
- Built-in pretty-printed HTML rendering support
- Extensible - works with any languge by supplying your own 'core'
- Write documents once and render it to multiple formats with ease
- Comes with cores for HTML and Markdown

## Examples
- Render a heading:
-       "Hello World" | h1
- Render a paragraph with a link:
-       "Click here" | link(href="https://example.com")
- Create this readme:
-       
      {# README.wtf #}
      {{
      (
          "WTFScript"
              | h1
          ~ "Web Template Format Script Engine"
              | h2
          ~ (
              "WTFScript is a Jinja2-based macro rendering engine for building structured "
              "content using custom-defined filters and aliases. Macros are stored as "
              ".template files with arguments specified via dummy functions for argument validation.\n\n"
          )   | paragraph
          ~ (
              "Features"
                  | h2
              ~ (
                  "Macro-based rendering using Jinja2 filters"
                  , "A simple system to create your own 'cores' for custom languages, or theming"
                  , "Built-in pretty-printed HTML rendering support" 
                  , "Extensible - works with any languge by supplying your own 'core'"
                  , "Write documents once and render it to multiple formats with ease"
                  , "Comes with cores for HTML and Markdown"
                  )   | unorderedlist
          )
          ~ (
              "Examples"
                  | h2
              ~ (
                  "Render a heading:"
                  , '"Hello World" | h1'
                      | codeblock
                  , "Render a paragraph with a link:"
                  , '"Click here" | link(href="https://example.com")'
                      | codeblock
                  , "Create this readme:"
                  , ("\n{# README.wtf #}\n"+wtf_script.strip()).split("\n")
                      | jacc(codeblock, join_string="\n")
                  , "Render this readme:"
                  , ("\n{# WTFScript.py #}\n"+py_script.strip()).split("\n")
                      | jacc(codeblock, join_string="\n")
              )   | unorderedlist
          )
          ~ (
              "Core System"
                  | h2
              ~ "These functions are available in all WTF namespaces\n"
                  | paragraph
              ~ (
                  "acc / accumulate – Apply a function to a list of items"
                  , "cattr / collect_attribute – Collect attributes from a list of objects"
                  , "jacc / join_accumulate – Apply and join results"
                  , "jcattr / join_collect_attribute – Collect and join attributes"
                  , "sacc / step_accumulate – Group and process lists in steps"
                  , "flas / flatten_structure - Flatten nested lists in the form [(depth, content), ...]"
              )   | unorderedlist
              
              ~ "3 built-in renderers\n"
                  | h5
              ~ (
                  "HTML\n"
                      | h6,
                  (
                      "Integrated pretty-printer"
                      , "Works great with Flask and SQLAlchemy"
                      , "from WTFScript import WTFHTML as WTF"
                          | code
                      , ("\n{# example.html.wtf #}\n"+html_script.strip()).split("\n")
                          | jacc(codeblock, join_string="\n  ")
                  ),
                  "Markdown\n"
                      | h6,
                  (
                      "Great for generating readme files"
                      , "Useful for generating simple markdown to inject into Flask"
                      , "from WTFScript import WTFMD as WTF"
                          | code
                  )
              )   | unorderedlist
          ) 
          ~ hr()
          ~ "WTF? - That was easy!"
              | paragraph
              | b
      ) | safe
      }}
- Render this readme:
-       
      {# WTFScript.py #}
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

## Core System
These functions are available in all WTF namespaces
- acc / accumulate – Apply a function to a list of items
- cattr / collect_attribute – Collect attributes from a list of objects
- jacc / join_accumulate – Apply and join results
- jcattr / join_collect_attribute – Collect and join attributes
- sacc / step_accumulate – Group and process lists in steps
- flas / flatten_structure - Flatten nested lists in the form [(depth, content), ...]

##### 3 built-in renderers

- ###### HTML


  - Integrated pretty-printer
  - Works great with Flask and SQLAlchemy
  - `from WTFScript import WTFHTML as WTF`
  -       
        {# example.html.wtf #}
        {{
        (
            doctype()
            ~(
                "Hello World"
                    | title
                ~ link(
                    rel="stylesheet",
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css",
                    crossorigin="anonymous"
                )
                ~ style(
                    "html, body { height: 100%; margin: 0; padding: 0; }"
                )
            ) | head
            ~ (
                "Hello!"
                    | h2
                    | div("card-header card-dark")
                ~ (
                    "Some\tpreformatted         text"
                        | pre
                        | div
                    ~ (
                        "Here's a list"
                        ~ range(10)
                            | jacc(li)
                            | ol
                    )   | div
                )   | div("col")
                    | div("card-body")
            ) | div("card shadow", style="width: 70vw; max-width: 600px;")
                | div("d-flex justify-content-center align-items-center h-100")
                | body("h-100")
            ~ script(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js",
                crossorigin="anonymous"
            )
        ) | html("h-100")
        }}
- ###### Markdown


  - Great for generating readme files
  - Useful for generating simple markdown to inject into Flask
  - `from WTFScript import WTFMD as WTF`



---

**WTF? - That was easy!**