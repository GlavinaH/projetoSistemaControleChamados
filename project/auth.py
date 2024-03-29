from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template("inscricao.html")

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/inicio')
def inicio():
    return render_template("inicio.html")

@auth.route('/meus_equipamentos')
def meus_equipamentos():
    return render_template("meus_equipamentos.html")

@auth.route('/criar_equipamento')
def criar_equipamento():
    return render_template("criar_equipamento.html")