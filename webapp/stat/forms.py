""" Recommend form """
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import Form, FieldList, FormField, IntegerField, SelectField, \
        StringField, TextAreaField, SubmitField
from wtforms import validators


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


class LapForm(Form):
    """ Subform """
    ingredient = StringField('ингредиент',
                             validators=[DataRequired(), validators.Length(max=150)],
                             render_kw={"class": "form-control"})
    how_much = StringField('сколько',
                           validators=[DataRequired(), validators.Length(max=150)],
                           render_kw={"class": "form-control"})


class RecipeForm(FlaskForm):
    """ class RecommendForm """
    dish = StringField("Название блюда",
                       validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    directions = StringField("Рецепт",
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    rows = FieldList(FormField(LapForm), min_entries=1)
    submit = SubmitField("сохранить", render_kw={"class": "btn btn-primary"})


class NumberOfIngredientsForm(FlaskForm):
    """ class RecommendForm """
    number = IntegerField("Сколько ингредиентов в рецепте блюда",
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField("сохранить", render_kw={"class": "btn btn-primary"})


class VotingForm(FlaskForm):
    """ class RecommendForm """
    stars = IntegerField("Оценка",
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField("сохранить", render_kw={"class": "btn btn-primary"})
