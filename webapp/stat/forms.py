""" Recommend form """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RecommendByTypeForm(FlaskForm):
    """ class RecommendForm """
    search = StringField("Что искать",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    dish_type = StringField("Тип блюда",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    submit = SubmitField("порекоммендовать", render_kw={"class": "btn btn-primary"})


class RecommendCuisineForm(FlaskForm):
    """ class RecommendForm """
    search = StringField("Что искать",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    cuisine = StringField("Тип кухни",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    submit = SubmitField("порекоммендовать", render_kw={"class": "btn btn-primary"})
