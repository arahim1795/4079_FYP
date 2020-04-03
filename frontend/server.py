from flask import Flask, render_template, url_for, flash, redirect, session, request
from frontend.forms import URLForm

from backend.Annotator import Annotator
from backend.data.Scraper import Scraper

# backend
annotator = Annotator()
scraper = Scraper()

# frontend
app = Flask(__name__)
app.config["SECRET_KEY"] = "a95cb72c3c3d74b5f1ba2b24703a936e"


@app.route("/", methods=["GET", "POST"])
def main():
    form = URLForm()
    if form.validate_on_submit():
        flash(f"Success for {form.url.data}!", "success")
        session["url"] = form.url.data
        return redirect(url_for("view"))
    return render_template("main.html", form=form)


@app.route("/view")
def view():
    article = scraper._download_article(session["url"])
    annotated = annotator.server_annotation(article[2], "auto_annotated")
    return render_template("view.html", background="interlaced", article=article, annotated=annotated)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)
