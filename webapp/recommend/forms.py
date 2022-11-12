"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    Recommendation forms
"""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import IntegerField, SubmitField


class VotingForm(FlaskForm):
    """ class VotingForm """
    stars = IntegerField("Оценка",
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    submit = SubmitField("сохранить", render_kw={"class": "btn btn-primary"})
