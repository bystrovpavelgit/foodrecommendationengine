"""blueprint for statistics"""
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_required
from webapp.stat.forms import RecommendByTypeForm, RecommendCuisineForm

blueprint = Blueprint("stat", __name__, url_prefix="/stat")


@blueprint.route("/recommend")
def recommend():
    """ simple recommendation """
    title = "Dish Recommendation"
    return render_template("stat/recipes.html", title=title, message1="рецепт блюда",
                           message2="", message3="")


@blueprint.route("/search_by_type")
@login_required
def search_by_type():
    """ recommendation by type """
    title = "Dish Recommendation"
    form = RecommendByTypeForm()
    return render_template("stat/search_by_type.html", title=title, form=form)


@blueprint.route("/process_search_by_type", methods=["POST"])
def process_search_by_type():
    """ process_search_by_type endpoint """
    form = RecommendByTypeForm()
    if form.validate_on_submit():
        return redirect("/stat/recommend")
    flash("Незаполненные поля на форме")
    return redirect(url_for("stat.search_by_type"))


@blueprint.route("/search_cuisine")
def search_cuisine():
    """ simple cuisine recommendation """
    title = "Dish Recommendation"
    form = RecommendCuisineForm()
    return render_template("stat/search_cuisine.html", title=title, form=form)


@blueprint.route("/process_search_cuisine", methods=["POST"])
def process_search_cuisine():
    """ process_search_cuisine endpoint """
    form = RecommendCuisineForm()
    if form.validate_on_submit():
        return redirect("/stat/recommend")
    flash("Незаполненные поля на форме")
    return redirect(url_for("stat.search_cuisine"))
