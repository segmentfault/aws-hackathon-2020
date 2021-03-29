from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class Form(FlaskForm):
    symptom = StringField('symptom', render_kw={'id': 'symptom'})
    submit = SubmitField('提交', render_kw={'id': 'submit', 'class': 'submit'})

