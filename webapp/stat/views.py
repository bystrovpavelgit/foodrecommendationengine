"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    blueprint for statistics
"""
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_wtf import FlaskForm
import logging
from wtforms import FormField, FieldList, StringField, SubmitField
from wtforms.validators import DataRequired
from webapp.business_logic import insert_recipe_data, \
    find_recipe_id_by_type_and_cuisine
from webapp.dl import predict_types
from webapp.stat.forms import NumberOfIngredientsForm, LapForm
from webapp.config import VALID_CUISINE, TYPE_MAP, FILL_RECIPE,\
    INGREDIENTS_NUM

blueprint = Blueprint("stat", __name__, url_prefix="/stat")


def create_template_form(num):
    """ create template form with min_entries = num"""

    class RecipeForm2(FlaskForm):
        """ class RecipeForm2 """
        dish = StringField("Название блюда",
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
        directions = StringField("Рецепт",
                                 validators=[DataRequired()],
                                 render_kw={"class": "form-control"})
        rows = FieldList(FormField(LapForm), min_entries=num)
        submit = SubmitField("сохранить", render_kw={"class": "btn btn-primary"})

    form = RecipeForm2()
    return form


@blueprint.route("/fill_recipe/<int:num>", methods=["GET", "POST"])
def fill_recipe(num):
    """ simple cuisine recommendation """
    form = create_template_form(num)
    if request.method == "POST":
        if form.validate_on_submit():
            ingredients = f"{[el['ingredient'] for el in form.rows.data]}"
            mera = f"{[el['how_much'] for el in form.rows.data]}"
            data = [{"name": form.dish.data,
                     "pic_url": "",
                     "pic": "",
                     "ingredients": ingredients,
                     "mera": mera,
                     "directions": f"[{form.directions.data}]",
                     "cusine": "",
                     "typed": "",
                     "url": "manual"}]
            cuisine, type_ = predict_types(data)
            data[0]["cusine"] = cuisine
            data[0]["typed"] = type_
            insert_recipe_data(data)
            flash(f"Рецепт сохранен - Тип {type_} кухня {cuisine}")
            return render_template("index.html")
        flash("Ошибка валидации")
        return redirect(f"/stat/fill_recipe/{num}")
    return render_template("stat/input_form.html", num=num, title=FILL_RECIPE, form=form)


@blueprint.route("/search_cuisine", methods=["GET", "POST"])
def search_cuisine():
    """ simple cuisine recommendation """
    title = "Dish Recommendation"
    if request.method == "POST":
        dish = request.form.get("dish")
        cuisine = request.form.get("cuisine")
        if dish in TYPE_MAP.keys() and cuisine in VALID_CUISINE:
            dish_id = find_recipe_id_by_type_and_cuisine(dish, cuisine)
            return redirect(f"/recommend/recipe/{dish_id}")
        logging.warning(f"Ошибка валидации dish_type:{dish} cuisine:{cuisine}")
        flash("Ошибка валидации")
        return redirect(url_for("stat.search_cuisine"))
    return render_template("stat/search_cuisine.html", title=title)


@blueprint.route("/new_recipe", methods=["GET", "POST"])
def new_recipe():
    """ simple cuisine recommendation """
    form = NumberOfIngredientsForm()
    if request.method == "POST":
        if form.validate_on_submit():
            num = int(form.number.data)
            return redirect(f"/stat/fill_recipe/{num}")
        flash("Ошибка валидации")
        return redirect(url_for("stat.new_recipe"))
    return render_template("stat/input_number.html", title=INGREDIENTS_NUM, form=form)
