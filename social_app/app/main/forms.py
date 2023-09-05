from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    """
    This class will be rendered to present the
    with a form to fill in
    """
    name = StringField("What's you name buddy", validators=[DataRequired()])
    submit = SubmitField('Submit')
