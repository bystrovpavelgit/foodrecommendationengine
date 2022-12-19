"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    blueprint for recommendations
"""
from flask import render_template, Blueprint, redirect, \
    url_for, flash
from flask_login import login_required
from webapp.business_logic import save_users_ratings
from webapp.utils.recipes_util import calculate_embeddings
from webapp.config import CALC_MODEL
from webapp.calculate.forms import CalcForm

blueprint = Blueprint("calculate", __name__, url_prefix="/calculate")


@blueprint.route("/calculate")
@login_required
def calculate():
    """ show calculate form """
    form = CalcForm()
    return render_template("calculate/calculate.html",
                           title=CALC_MODEL,
                           form=form)


@blueprint.route("/process_calculate", methods=["POST"])
@login_required
def process_calculate():
    """ calculate embeddings for CF-model"""
    form = CalcForm()
    if form.validate_on_submit():
        save_users_ratings(file_name="data/users_ratings.csv")
        calculate_embeddings()
        flash("модель повторно рассчитана")
        return redirect(url_for("index"))
    flash("Ошибка в calculate form")
    return redirect(url_for("calculate.calculate"))
