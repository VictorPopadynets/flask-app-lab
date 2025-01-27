from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField("Ім’я", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Телефон")
    group_id = SelectField("Група", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Зберегти")
