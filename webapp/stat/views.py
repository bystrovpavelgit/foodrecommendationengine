"""blueprint for statistics"""
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FormField, FieldList, StringField, SubmitField
from wtforms.validators import DataRequired
from webapp.business_logic import insert_recipe_data, add_rating_for_author
from webapp.dl import predict_types
from webapp.stat.forms import RecommendByTypeForm, RecommendCuisineForm, \
    NumberOfIngredientsForm, LapForm, VotingForm

blueprint = Blueprint("stat", __name__, url_prefix="/stat")


@blueprint.route("/recommends")
def recommend():
    """ simple recommendation """
    title = "Dish Recommendation"
    return render_template("stat/recipes.html", title=title, message1="рецепт блюда",
                           message2="", message3="")


@blueprint.route('/recommend/<int:num>')
def get(num):
    """ simple recommendation """
    title = "Dish Recommendation"
    arr = [f"{num} Марокканский суп с нутом и имбирем",
           "Морковь, лук, чеснок нарезать, имбирь натереть на мелкой терке. Обжарить овощи" +
           " на растительном масле до мягкости.",
           "Чеснок 1 зубчик, Морковь 2 штуки, Репчатый лук 1 головка"]
    return render_template("stat/recipe.html", title=title,
                           answers=arr,
                           chart_img="/5.jpg")


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


@blueprint.route("/search_cuisine", methods=["GET", "POST"])
def search_cuisine():
    """ simple cuisine recommendation """
    title = "Dish Recommendation"
    form = RecommendCuisineForm()
    if request.method == "POST":
        if form.validate_on_submit():
            arr = ["Марокканский суп с нутом и имбирем",
                   "Морковь, лук, чеснок нарезать, имбирь натереть на мелкой терке. Обжарить овощи" +
                   " на растительном масле до мягкости.",
                   "Чеснок 1 зубчик, Морковь 2 штуки, Репчатый лук 1 головка"]
            return render_template("stat/recipe.html", main_img="/5.jpg", answers=arr)
        flash("Ошибка валидации")
        return redirect(url_for("stat.search_cuisine"))
    return render_template("stat/search_cuisine.html", title=title, form=form)


@blueprint.route("/new_recipe", methods=["GET", "POST"])
@login_required
def new_recipe():
    """ simple cuisine recommendation """
    title = "How many ingredients"
    form = NumberOfIngredientsForm()
    if request.method == "POST":
        if form.validate_on_submit():
            num = int(form.number.data)
            return redirect(f"/stat/fill_recipe/{num}")
        flash("Ошибка валидации")
        return redirect(url_for("stat.new_recipe"))
    return render_template("stat/input_number.html", title=title, form=form)


@blueprint.route("/fill_recipe/<int:num>", methods=["GET", "POST"])
@login_required
def fill_recipe(num):
    """ simple cuisine recommendation """

    class RecipeForm2(FlaskForm):
        """ class RecommendForm """
        dish = StringField("Название блюда",
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
        directions = StringField("Рецепт",
                                 validators=[DataRequired()],
                                 render_kw={"class": "form-control"})
        rows = FieldList(FormField(LapForm), min_entries=num)
        submit = SubmitField("сохранить", render_kw={"class": "btn btn-primary"})
    title = "Fill Recipe"
    form = RecipeForm2()
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
            flash(f"Данные сохранены")
            return render_template("index.html")
        flash("Ошибка валидации")
        return redirect(f"/stat/fill_recipe/{num}")
    return render_template("stat/input_form.html", num=num, title=title, form=form)


@blueprint.route("/rate_recipe/<int:rec_id>", methods=["GET", "POST"])
@login_required
def rate_recipe(rec_id):  # TO_DO make small window in window vote
    """ simple cuisine recommendation """
    title = "How many ingredients"
    form = VotingForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = current_user
            recipe_id = int(rec_id)
            add_rating_for_author(int(form.stars.data), user.username, recipe_id)
            flash(f"Данные сохранены")
            return render_template("index.html")
        flash("Ошибка валидации")
        return redirect(f"/stat/rate_recipe/{rec_id}")
    return render_template("stat/rate_recipe.html", rec_id=rec_id, title=title, form=form)
