from flask import Blueprint, render_template, redirect, flash, url_for, request
from . import db
from .models import Equipamento
import psycopg2
import psycopg2.extras

main = Blueprint('main', __name__)

DB_HOST = "dbcontrolechamados.cb4akgeqo179.us-east-1.rds.amazonaws.com"
DB_NAME = "db-controle-chamados"
DB_USER = "postgres"
DB_PASS = "controle123"
DB_PORT = "5432"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/profile')
def profile():
    return 'Profile'

@main.route('/submit', methods=['POST'])
def submit():
    marca = request.form['marca']
    modelo = request.form['modelo']
    numero_serie = request.form['numero_serie']

    equipamento = Equipamento(marca,modelo,numero_serie)
    db.session.add(equipamento)
    db.session.commit()
    flash("Equipamento adicionado com sucesso.")
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM tb_equipamentos"
    cur.execute(s)
    lista_equipamentos=cur.fetchall()
    return render_template("meus_equipamentos.html", lista_equipamentos=lista_equipamentos)

@main.route('/meus_equipamentos')
def meus_equipamentos():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM tb_equipamentos ORDER BY id_equip ASC"
    cur.execute(s)
    lista_equipamentos=cur.fetchall()
    return render_template("meus_equipamentos.html", lista_equipamentos=lista_equipamentos)

@main.route('/edit/<id>', methods=['POST','GET'])
def get_equipamento(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_equipamentos WHERE id_equip={id}')  
    data=cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editar_equipamento.html', equipamento=data[0])

@main.route('/update/<id>', methods=['POST'])
def update_equip(id):
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f'''UPDATE tb_equipamentos
                        SET marca='{marca}',
                        modelo='{modelo}',
                        numero_serie='{numero_serie}'
                        WHERE id_equip={id}''')
        cur.execute('SELECT * FROM tb_equipamentos ORDER BY id_equip ASC')       
        flash("Equipamento atualizado com sucesso.")
        conn.commit()
        return redirect(url_for('main.meus_equipamentos'))
    
@main.route('/delete/<id>', methods=['POST','GET'])
def delete_equip(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'DELETE FROM tb_equipamentos WHERE id_equip={id}')
    conn.commit()
    flash('Equipamento removido com sucesso')
    return redirect(url_for('main.meus_equipamentos'))