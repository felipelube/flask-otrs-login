from wtforms import Form, RadioField, TextField, PasswordField, validators
from flask import Flask, render_template, request, make_response, redirect
from flask_wtf import FlaskForm
from dotenv import load_dotenv
import requests
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
        otrs_data = {
            'User': form.username.data,
            'Password': form.password.data,
            'Action': 'Login',
            'RequestedURL': None,
            'Lang': 'en',
            'TimeZoneOffset': 180  # TODO
        }
        # TODO: reinserir os parâmetros da url recebidos do otrs em caso de
        # redirecionamento
        with requests.post('http://localhost/otrs/index.pl',
                           data=otrs_data, allow_redirects=False) as r:
            if (r.status_code == 302
                    and r.cookies.get('OTRSAgentInterface', None)):
                response = redirect('http://localhost'+r.headers['location'])
                # TODO: definir os outros parâmetros (host, expires etc.) de
                # set_cookie respeitando os dados do cookie recebido.
                response.set_cookie('OTRSAgentInterface',
                                    r.cookies['OTRSAgentInterface'])
                return response
            # TODO: tratar outros casos: 200 (falha na autenticação), 500 etc
            # TODO: Pegar a mensagem de erro do OTRS e inserir ela no nosso
            # formulário (usar o beautifulsoup para pegar o texto do elemento
            # .LoginBox>.ErrorBox>span)
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run()
