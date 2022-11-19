"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    blueprint for recommendations
"""
from flask import abort, render_template, Blueprint, request, redirect, \
    url_for, flash
from flask_login import login_required, current_user
import logging
from webapp.business_logic import find_recipe, \
    insert_or_update_rating
from webapp.utils.recipes_util import find_enough_recommended_recipes, \
    calculate_embeddings, to_list
from webapp.config import RECOMMEND_ACTIONS, COLORS, RECOMMEND_ACT, \
    RATE_ACT, RATE_ACTIONS, VALID_CUISINE, TYPE_MAP, RECIPE, CALC_MODEL
from webapp.recommend.forms import CalcForm


blueprint = Blueprint("recommend", __name__, url_prefix="/recommend", static_url_path="/", static_folder="/")


def fill_params(type_):
    """ fill mandatory params """
    if type_ in TYPE_MAP.keys():
        dish_type = type_
        text = f"Рецепты с типом {type_}".upper()
        cuisine = None
    else:
        dish_type = None
        text = f"{type_} кухня".upper()
        cuisine = type_
    return dish_type, cuisine, text


def find_index_of_form(form, actions, action):
    """ find index of form function """
    try:
        index = actions.index(form.get(action))
        return index
    except ValueError:
        logging.error(f"Value Error in find_index_of_form: {form} {actions} {action}")
        return None


def endpoint_template(params, method, type_, valid_list):
    """ endpoint template для рекоммендации по типу блюда или по кухне
    параметры:
        params     - tuple (russian_type, english_type, redirect_url, html)
                       redirect_url: URL для редиректа в случае успеха
                       html: путь к html-странице для GET-request
        method     - GET / POST
        type_      - form type
        valid_list - набор корректных значений
    """
    title = f"Выбор {params[0]}"
    if method == "POST":
        if type_ in valid_list:
            logging.info(f"{params[1]}{type_}")
            return redirect(f"{params[1]}{type_}")
        logging.warning(f"Введен некорректный тип: {type_}")
        flash(f"Введите корректный тип {params[0]}")
    return render_template(f"{params[2]}", title=title, select=title)


@blueprint.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():
    """ recipe recommendation by cuisine """
    params = ("кухни", "/recommend/recipes/", "recommend/select_cuisine.html")
    type_ = request.form.get("cuisine") if request.method == "POST" else ""
    return endpoint_template(params,
                             request.method,
                             type_,
                             VALID_CUISINE
                             )


@blueprint.route("/recommend_by_type", methods=["GET", "POST"])
@login_required
def recommend_by_type():
    """ recipe recommendation by type """
    params = ("типа блюда", "/recommend/recipes/", "recommend/select_type.html")
    type_ = request.form.get("dish") if request.method == "POST" else ""
    return endpoint_template(params,
                             request.method,
                             type_,
                             TYPE_MAP.keys()
                             )


@blueprint.route("/recipes/<string:type_>", methods=["GET", "POST"])
@login_required
def recipes(type_):
    """ recipe recommendation """
    title = "Dish Recommendation"
    user = current_user
    dish_type, cuisine, text = fill_params(type_)
    messages, ids = find_enough_recommended_recipes(user.id, cuisine, dish_type)
    messages = messages[:9]
    ids = ids[:9]
    if request.method == "POST":
        index = find_index_of_form(request.form,
                                   RECOMMEND_ACTIONS, RECOMMEND_ACT)
        if index is not None:
            logging.info(f"user:{user.id} /recommend/recipe/{ids[index]}")
            return redirect(f"/recommend/recipe/{ids[index]}")
        flash("Ошибка валидации")
        return abort(404)
    print(ids)
    return render_template("recommend/recipes.html",
                           title=title,
                           text=text,
                           messages=messages,
                           type_=type_)


@blueprint.route('/recipe/<int:num>', methods=["GET", "POST"])
@login_required
def recipe(num):
    """ show simple recipe with ingedients table """
    rec = find_recipe(num)
    if request.method == "POST":
        if rec:
            index = find_index_of_form(request.form,
                                       RATE_ACTIONS,
                                       RATE_ACT)
            if index is not None:
                index += 1
                user = current_user
                insert_or_update_rating(int(index), user.username, int(num))
                flash(f"Данные сохранены")
                logging.info(f"user:{user.id} /recommend/recipe/{num}")
                return redirect(f"/recommend/recipe/{num}")
        flash("Ошибка валидации или Ошибка поиска рецепта")
        return redirect(url_for("index"))
    if rec:
        arr = [rec.name,
               rec.typed] + [" ".join(to_list(rec.directions))]
        ingr = to_list(rec.ingredients)
        zipped = zip([COLORS[i % 5] for i in range(len(ingr))],
                     ingr,
                     to_list(rec.mera))
        return render_template("recommend/show_recipe.html",
                               main_text=RECIPE,
                               num=num,
                               messages=arr,
                               items=zipped)
    logging.error(f"Ошибка: рецепт {num} не найден")
    flash(f"Ошибка: рецепт {num} не найден")
    return redirect(url_for("index"))


@blueprint.route("/calculate")
@login_required
def calculate():
    """ show calculate form """
    form = CalcForm()
    return render_template("recommend/calculate.html", title=CALC_MODEL, form=form)


@blueprint.route("/process_calculate", methods=["POST"])
@login_required
def process_calculate():
    """ process embeddings for CF-model"""
    form = CalcForm()
    if form.validate_on_submit():
        calculate_embeddings()
        logging.info(f"модель повторно рассчитана")
        flash("модель повторно рассчитана")
        return redirect(url_for("index"))
    flash("Ошибка")
    return redirect(url_for("recommend.calculate"))
