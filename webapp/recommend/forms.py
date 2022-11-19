"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    Recommendation forms
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField


class CalcForm(FlaskForm):
    """ Calc Form """
    ok = SubmitField("OK", render_kw={"class": "btn btn-primary"})
