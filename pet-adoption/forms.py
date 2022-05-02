from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf

class NewPetForm(FlaskForm):
    name = StringField("Pet name", validators=[InputRequired(message="Pet name cannot be blank")])
    species = StringField("Species", validators=[InputRequired(message="Species cannot be blank. Please provide a species of cat, dog or porcupine"), 
                AnyOf(["cat", "dog", "porcupine"])])
    photo_url = StringField("Photo URL", validators=[Optional(), URL(require_tld=False)])
    age = IntegerField("Age", validators=[Optional(), NumberRange(0,30,"Please input a age between 0 and 30")])
    notes = TextAreaField("Notes", validators=[Optional()])

class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL", validators=[Optional(), URL(require_tld=False)])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Available?")