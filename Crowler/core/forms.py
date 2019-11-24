from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

class FilterForm(FlaskForm):
    
    number_of_rooms = SelectField("Liczba Pokoi",
    choices = [("one", "Kawalerka"), ("two", "2 pokoje"), ("three", "3 pokoje"), ("four", "4 i więcej")], validators=[DataRequired()])
    price_from = IntegerField("Cena od", validators=[DataRequired()])
    price_to = IntegerField("Cena do", validators=[DataRequired()])
    localization = SelectField("Lokalizacja",
    choices = [("391", "Krzyki"), ("393", "Fabryczna"), ("389", "Psie Pole"), ("387", "Śródmieście"), ("385", "Stare Miasto")], validators=[DataRequired()])
    submit = SubmitField("Dalej")