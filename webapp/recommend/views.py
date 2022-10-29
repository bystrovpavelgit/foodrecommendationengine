"""blueprint for statistics"""
from flask import abort, render_template, Blueprint, request, redirect, \
    url_for, flash
from flask_login import login_required, current_user
from webapp.business_logic import find_recipe_names, find_recipe, insert_or_update_rating
from webapp.config import RECOMMEND_ACTIONS, COLORS, RECOMMEND_ACT, \
    RATE_ACT, RATE_ACTIONS
from webapp.utils.nlp_util import str_to_list

blueprint = Blueprint("recommend", __name__, url_prefix="/recommend")


def find_index_of_form(form, actions, action):
    """ find index of form function """
    try:
        index = actions.index(form.get(action))
        return index
    except ValueError:
        return None


@blueprint.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():
    """ recipe recommendation """
    title = "Dish Recommendation"
    messages, ids = find_recipe_names("русская")
    if request.method == "POST":
        index = find_index_of_form(request.form,
                                   RECOMMEND_ACTIONS, RECOMMEND_ACT)
        if index is not None:
            return redirect(f"/recommend/recipe/{ids[index]}")
        flash("Ошибка валидации")
        return abort(404)
    return render_template("recommend/recipes.html",
                           title=title,
                           messages=messages)


@blueprint.route('/recipe/<int:num>', methods=["GET", "POST"])
@login_required
def recipe(num):
    """ show simple recipe with ingedients table """
    title = "Dish"
    rec = find_recipe(num)
    if request.method == "POST":
        if rec:
            index = find_index_of_form(request.form,
                                       RATE_ACTIONS, RATE_ACT)
            if index is not None:
                print(f"RATING {index}")
                index += 1
                user = current_user
                insert_or_update_rating(int(index), user.username, int(num))
                flash(f"Данные сохранены")
                return redirect(f"/recommend/recipe/{num}")

        flash("Ошибка валидации или Ошибка поиска рецепта")
        return redirect(url_for("index"))
    if rec:
        arr = [rec.name,
               rec.typed] + [" ".join(str_to_list(rec.directions))]
        items = str_to_list(rec.ingredients)
        nums = str_to_list(rec.mera)
        zipped = zip([COLORS[i % 5] for i in range(len(nums))], items, nums)
        return render_template("recommend/show_recipe.html",
                               main_text=title,
                               num=num,
                               messages=arr,
                               items=zipped,
                               main_img="/5.jpg")

    flash("Ошибка: рецепт не найден")
    return redirect(url_for("index"))
