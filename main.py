from wtforms import Form, RadioField, TextField, PasswordField, validators
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


class LoginForm(FlaskForm):
    username = TextField('Nome de usuário', [validators.Required()])
    password = PasswordField('Senha', [validators.Required()])
    login_type = RadioField('Tipo de login', [validators.Required()],  choices=[
                            ("customer", "Cliente"), ("agent", "Agente")])


@app.route('/', methods=['GET', 'POST'])
def login_form():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        pass  # TODO
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run()
