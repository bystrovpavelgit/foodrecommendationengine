""" Recommendation forms """
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import IntegerField, SubmitField


class ViewForm(FlaskForm):
    """ class ViewForm """
    submit = SubmitField("view", render_kw={"class": "btn btn-primary"})


class VotingForm(FlaskForm):
    """ class VotingForm """
    stars = IntegerField("Оценка",
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    submit = SubmitField("сохранить", render_kw={"class": "btn btn-primary"})
