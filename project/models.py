from flask_login import UserMixin
from . import db

class Equipamento(db.Model):
    __tablename__ = 'tb_equipamentos'
    id_equip = db.Column(db.Integer,primary_key=True)    
    marca = db.Column(db.String(30))
    modelo = db.Column(db.String(30))
    numero_serie = db.Column(db.String(50))
    id_usuario = db.Column(db.Integer, db.ForeignKey('tb_usuarios.id'))
    
    def __init__(self,marca,modelo,numero_serie,id_usuario):
        self.marca=marca
        self.modelo=modelo
        self.numero_serie=numero_serie
        self.id_usuario=id_usuario


class Usuario(UserMixin, db.Model):
    __tablename__='tb_usuarios'
    id = db.Column(db.Integer,primary_key=True)    
    empresa = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))
    
    def __init__(self,empresa,endereco,cidade,estado,nome,telefone,email,senha):
        self.empresa = empresa
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.senha = senha     
        