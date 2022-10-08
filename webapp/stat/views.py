"""blueprint for statistics"""
from flask import render_template, Blueprint
from flask_login import login_required

blueprint = Blueprint("stat", __name__, url_prefix="/stat")


@blueprint.route("/recommend")
def simple_recommend():
    """ simple recommendation """
    title = "Dish Recommendation"
    return render_template("stat/recipes.html", title=title, message1="рецепт блюда",
           message2="", message3="")

