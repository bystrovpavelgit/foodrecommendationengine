"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    blueprint for recommendations
"""
from flask import render_template, Blueprint, request, redirect, \
    url_for, flash
from flask_login import login_required, current_user
import logging
from webapp.business_logic import find_recipe, \
    insert_or_update_rating
from webapp.utils.recipes_util import find_enough_recommended_recipes, \
    to_list
from webapp.config import RECOMMEND_ACTIONS, COLORS, RECOMMEND_ACT, \
    RATE_ACT, RATE_ACTIONS, VALID_CUISINE, TYPE_MAP, RECIPE, \
    RECOMMEND_RECIPES, USER_BASED, ITEM_BASED, \
    USER_BASED_RECOMMENDATION, ITEM_BASED_RECOMMENDATION

blueprint = Blueprint("recommend", __name__, url_prefix="/recommend")


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


def log_and_flash(msg):
    """ logging """
    logging.warning(f"Введен некорректный {msg}")
    flash(f"Введите корректный {msg}")


@blueprint.route("/recommend")
@login_required
def recommend():
    """ recipe recommendation by cuisine """
    return render_template("recommend/select_cuisine.html",
                           title="Выбор кухни")


@blueprint.route("/recommend", methods=["POST"])
@login_required
def process_recommend():
    """ process recipe recommendation by cuisine """
    type_ = request.form.get("cuisine")
    if type_ in VALID_CUISINE:
        return redirect(f"/recommend/recipes/{type_}/{USER_BASED}")
    log_and_flash(f"тип кухни: {type_}")
    return render_template("recommend/select_cuisine.html",
                           title="Выбор кухни")


@blueprint.route("/recommend_by_type")
@login_required
def recommend_by_type():
    """ recipe recommendation by type """
    return render_template("recommend/recommend_by_type_user_based.html",
                           title=USER_BASED_RECOMMENDATION)


@blueprint.route("/recommend_by_type", methods=["POST"])
@login_required
def process_recommend_by_type():
    """ process recipe recommendation by type """
    type_ = request.form.get("dish")
    if type_ in TYPE_MAP.keys():
        return redirect(f"/recommend/recipes/{type_}/{USER_BASED}")
    log_and_flash(f"тип: {type_} (user based filtration)")
    return render_template("recommend/recommend_by_type_user_based.html",
                           title=USER_BASED_RECOMMENDATION)


@blueprint.route("/recipes/<string:type_>/<string:filtering>")
@login_required
def recipes(type_, filtering):
    """ recipe recommendation """
    user = current_user
    dish_type, cuisine, text = fill_params(type_)
    messages, ids = find_enough_recommended_recipes(user.id, cuisine, dish_type)
    messages = messages[:9]
    return render_template("recommend/recipes.html",
                           title=RECOMMEND_RECIPES,
                           text=text,
                           messages=messages,
                           type_=type_,
                           filtering=filtering)


@blueprint.route("/recipes/<string:type_>/<string:filtering>", methods=["POST"])
@login_required
def process_recipes(type_, filtering):
    """ process recipe recommendation """
    user = current_user
    dish_type, cuisine, text = fill_params(type_)
    if filtering == USER_BASED:
        messages, ids = find_enough_recommended_recipes(user.id, cuisine, dish_type)
    elif filtering == ITEM_BASED:
        messages, ids = find_enough_recommended_recipes(user.id, cuisine, dish_type)
    else:
        flash(f"Неправильный тип фильтрации {filtering}")
        return redirect(url_for("index"))
    ids = ids[:9]
    index = find_index_of_form(request.form,
                               RECOMMEND_ACTIONS, RECOMMEND_ACT)
    if index is not None and len(ids) > index:
        if ids[index] >= 0:
            logging.info(f"user:{user.id} /recommend/recipe/{ids[index]}")
            return redirect(f"/recommend/recipe/{ids[index]}")
    flash("Ошибка валидации")
    return redirect(url_for("index"))


@blueprint.route('/recipe/<int:num>', methods=["GET"])
@login_required
def recipe(num):
    """ show simple recipe with ingedients table """
    rec = find_recipe(num)
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


@blueprint.route('/recipe/<int:num>', methods=["POST"])
@login_required
def process_recipe(num):
    """ show simple recipe with ingedients table """
    rec = find_recipe(num)
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
        else:
            msg = "Ошибка поиска рецепта"
    else:
        msg = "Ошибка валидации рецепта"
    flash(msg)
    return redirect(url_for("index"))


@blueprint.route("/recommend_by_type_item_based")
@login_required
def recommend_by_type_item_based():
    """ recipe recommendation by type """
    return render_template("recommend/recommend_by_type_item_based.html",
                           title=ITEM_BASED_RECOMMENDATION)


@blueprint.route("/recommend_by_type_item_based", methods=["POST"])
@login_required
def process_recommend_by_type_item_based():
    """ process recipe recommendation by type """
    type_ = request.form.get("dish")
    if type_ in TYPE_MAP.keys():
        return redirect(f"/recommend/recipes/{type_}/{ITEM_BASED}")
    log_and_flash(f"тип: {type_} (item based filtration)")
    return render_template("recommend/recommend_by_type_item_based.html",
                           title=ITEM_BASED_RECOMMENDATION)
