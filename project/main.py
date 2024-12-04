from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import db
from .models import Equipamento, Chamado
import psycopg2
import psycopg2.extras
from datetime import datetime

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

@main.route('/meus_equipamentos')
@login_required
def meus_equipamentos():
    id_usuario = current_user.id
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_equipamentos WHERE id_usuario={id_usuario} ORDER BY id_equip ASC')
    lista_equipamentos=cur.fetchall()
    return render_template("meus_equipamentos.html", lista_equipamentos=lista_equipamentos)

@main.route('/edit_equipamento/<id>', methods=['POST','GET'])
@login_required
def get_equipamento(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_equipamentos WHERE id_equip={id}')  
    data=cur.fetchall()
    cur.close()
    return render_template('editar_equipamento.html', equipamento=data[0])

@main.route('/update/<id>', methods=['POST'])
@login_required
def update_equip(id):
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        
        id_usuario = current_user.id
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f'''UPDATE tb_equipamentos
                        SET marca='{marca}',
                        modelo='{modelo}',
                        numero_serie='{numero_serie}'
                        WHERE id_equip={id}''')
        cur.execute(f'SELECT * FROM tb_equipamentos WHERE id_usuario={id_usuario} ORDER BY id_equip ASC')       
        flash("Equipamento atualizado com sucesso.")
        conn.commit()
        return redirect(url_for('main.meus_equipamentos'))
    
@main.route('/delete_equipamento/<id>', methods=['POST','GET'])
@login_required
def delete_equip(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'DELETE FROM tb_equipamentos WHERE id_equip={id}')
    conn.commit()
    flash('Equipamento removido com sucesso')
    return redirect(url_for('main.meus_equipamentos'))

@main.route('/criar_equipamento')
@login_required
def criar_equipamento():
    return render_template('criar_equipamento.html')
    
@main.route('/submit_equipamento', methods=['POST'])
@login_required
def submit():
    marca = request.form['marca']
    modelo = request.form['modelo']
    numero_serie = request.form['numero_serie']
    id_usuario = current_user.id

    equipamento = Equipamento(marca,modelo,numero_serie,id_usuario)
    db.session.add(equipamento)
    db.session.commit()
    flash("Equipamento adicionado com sucesso.")
    return redirect(url_for('main.meus_equipamentos'))
    
    
@main.route('/meus_chamados')
@login_required
def meus_chamados():
    id_usuario = current_user.id
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_chamados WHERE id_usuario={id_usuario} ORDER BY id_chamado ASC')
    lista_chamados=cur.fetchall()
    return render_template("meus_chamados.html", lista_chamados=lista_chamados)

@main.route('/criar_chamado', methods=["POST","GET"])
@login_required
def criar_chamado():
    id_usuario = current_user.id
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT id_equip FROM tb_equipamentos WHERE id_usuario={id_usuario} ORDER BY id_equip ASC')
    id_equipamentos=cur.fetchall()
    return render_template('criar_chamado.html', id_equipamentos=id_equipamentos)

@main.route('/submit_chamado', methods=['POST'])
@login_required
def submit_chamado():
    garantia = request.form['opcoesGarantia']
    descricao_erro = request.form['descricao']
    id_equip = request.form['idEquip']
    id_usuario = current_user.id
    data_criacao = datetime.now()
    status_chamado = "Em aberto"

    chamado = Chamado(garantia, descricao_erro, id_equip, id_usuario, data_criacao, status_chamado)
    db.session.add(chamado)
    db.session.commit()
    flash("Chamado criado com sucesso.")
    return redirect(url_for('main.meus_chamados'))
    
@main.route('/adm_chamados')
@login_required
def adm_chamados():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_chamados ORDER BY id_chamado ASC')
    lista_chamados=cur.fetchall()
    return render_template("adm_chamados.html", lista_chamados=lista_chamados)

@main.route('/adm_edit_chamado/<id>', methods=['POST','GET'])
@login_required
def get_chamado(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_chamados WHERE id_chamado={id}')  
    data_chamado=cur.fetchall()
    cur.close()
    id_usuario_chamado = data_chamado[0][3]
    id_equipamento_chamado = data_chamado[0][2]
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_usuarios WHERE id={id_usuario_chamado}')  
    data_usuario=cur.fetchall()
    cur.close()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_equipamentos WHERE id_equip={id_equipamento_chamado}')  
    data_equipamento=cur.fetchall()
    cur.close()
    return render_template('adm_editar_chamado.html', data_chamado=data_chamado[0], data_usuario=data_usuario[0], data_equipamento=data_equipamento[0])

@main.route('/adm_update_chamado/<id>', methods=['POST'])
@login_required
def update_chamado(id):
    if request.method == 'POST':
        status_chamado = request.form['statusChamado']
                
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f'''UPDATE tb_chamados
                        SET status_chamado='{status_chamado}'
                        WHERE id_chamado={id}''')
        cur.execute(f'SELECT * FROM tb_chamados ORDER BY id_equip ASC')       
        flash("Status do chamado atualizado com sucesso.")
        conn.commit()
        return redirect(url_for('main.adm_chamados'))