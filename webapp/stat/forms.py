""" Recommend form """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RecommendForm(FlaskForm):
    """ class RecommendForm """
    dish_type = StringField("Тип блюда",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    recipe_type = StringField("К какой кухне относится рецепт",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    submit = SubmitField("searcht", render_kw={"class": "btn btn-primary"})
