from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from .auth import auth as auth_blueprint
from .main import main as main_blueprint

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
    
    return render_template('meus_equipamentos.html')



