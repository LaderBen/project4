from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import validators
from wtforms.fields import *

class csv_upload(FlaskForm):
    file = FileField(validators=[FileRequired(),FileAllowed(['csv'], 'csv file only')])

    submit = SubmitField()