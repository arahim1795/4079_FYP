from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators


class URLForm(FlaskForm):
    url = StringField(
        "URL",
        validators=[
            validators.DataRequired(),
            validators.URL(message="Valid URL is required."),
        ],
        render_kw={"placeholder": "Enter URL"},
    )

    submit = SubmitField("Analyse")
