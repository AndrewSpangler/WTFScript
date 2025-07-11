import os
from flask import Flask, request
from WTFScript import WTFHtmlFlask

app = Flask(__name__)
wtf = WTFHtmlFlask(app)
bootstrap_dir = os.path.join(os.path.dirname(__file__), "macros/html/bootstrap")
wtf.load_macros_dir(bootstrap_dir)

@app.route("/", methods=["GET", "POST"])
def previewer():
    content = request.form.get("content", "")
    if request.method == "POST":
        return wtf.render(content)
    return wtf.render_template("./previewer.html.wtf")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)