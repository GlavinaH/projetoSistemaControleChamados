from flask import Blueprint, render_template, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario
from . import db


auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template("inscricao.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    
    empresa = request.form.get('empresa')
    endereco = request.form.get('endereco')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario:
        flash('E-mail já existe')
        return redirect(url_for('auth.signup'))
    
    novo_usuario = Usuario(empresa=empresa, endereco=endereco, cidade=cidade, estado=estado, nome=nome, telefone=telefone, email=email, senha=generate_password_hash(senha, method='pbkdf2', salt_length=8))
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return redirect(url_for("auth.login"))

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/inicio')
def inicio():
    return render_template("inicio.html")

@auth.route('/criar_equipamento')
def criar_equipamento():
    return render_template("criar_equipamento.html")

