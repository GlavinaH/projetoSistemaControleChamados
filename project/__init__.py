from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from .auth import auth as auth_blueprint
from .main import main as main_blueprint
import psycopg2
import psycopg2.extras

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'p857111c9c9e05eb3cd3d6b18fa738a29777ab76760b6812a5079e938f8083589'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ud46diq0e2643u:p857111c9c9e05eb3cd3d6b18fa738a29777ab76760b6812a5079e938f8083589@cb4l59cdg4fg1k.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1le26gb6kv12a'
    
    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)

    return app

app = create_app()

db = SQLAlchemy(app)

DB_HOST="cb4l59cdg4fg1k.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
DB_NAME="d1le26gb6kv12a"
DB_USER="ud46diq0e2643u"
DB_PASS="p857111c9c9e05eb3cd3d6b18fa738a29777ab76760b6812a5079e938f8083589"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

class Equipamento(db.Model):
    __tablename__='tb_equipamentos'
    id_equip=db.Column(db.Integer,primary_key=True)    
    marca=db.Column(db.String(30))
    modelo=db.Column(db.String(30))
    numero_serie=db.Column(db.String(50))
    

    def __init__(self,marca,modelo,numero_serie):
        self.marca=marca
        self.modelo=modelo
        self.numero_serie=numero_serie

@app.route('/submit', methods=['POST'])
def submit():
    marca=request.form['marca']
    modelo=request.form['modelo']
    numero_serie=request.form['numero_serie']

    equipamento=Equipamento(marca,modelo,numero_serie)
    db.session.add(equipamento)
    db.session.commit()
    flash("Equipamento adicionado com sucesso.")
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM tb_equipamentos"
    cur.execute(s)
    lista_equipamentos=cur.fetchall()
    return render_template("meus_equipamentos.html", lista_equipamentos=lista_equipamentos)

@app.route('/meus_equipamentos')
def meus_equipamentos():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM tb_equipamentos ORDER BY id_equip ASC"
    cur.execute(s)
    lista_equipamentos=cur.fetchall()
    return render_template("meus_equipamentos.html", lista_equipamentos=lista_equipamentos)

@app.route('/edit/<id>', methods=['POST','GET'])
def get_equipamento(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM tb_equipamentos WHERE id_equip={id}')  
    data=cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editar_equipamento.html', equipamento=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_equip(id):
    if request.method == 'POST':
        marca=request.form['marca']
        modelo=request.form['modelo']
        numero_serie=request.form['numero_serie']
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f'''UPDATE tb_equipamentos
                        SET marca='{marca}',
                        modelo='{modelo}',
                        numero_serie='{numero_serie}'
                        WHERE id_equip={id}''')
        cur.execute('SELECT * FROM tb_equipamentos ORDER BY id_equip ASC')       
        flash("Equipamento atualizado com sucesso.")
        conn.commit()
        return redirect(url_for('meus_equipamentos'))
    
@app.route('/delete/<id>', methods=['POST','GET'])
def delete_equip(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'DELETE FROM tb_equipamentos WHERE id_equip={id}')
    conn.commit()
    flash('Equipamento removido com sucesso')
    return redirect(url_for('meus_equipamentos'))