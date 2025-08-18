from . import db
from datetime import datetime

class Cliente(db.Model):
    """Modelo para os clientes."""
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=True)

    respostas = db.relationship('Resposta', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.email}>'

class Pesquisa(db.Model):
    """Modelo para as pesquisas de NPS."""
    __tablename__ = 'pesquisas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    respostas = db.relationship('Resposta', backref='pesquisa', lazy=True)

    def __repr__(self):
        return f'<Pesquisa {self.nome}>'

class Resposta(db.Model):
    """Modelo para as respostas dos clientes."""
    __tablename__ = 'respostas'

    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    data_resposta = db.Column(db.DateTime, default=datetime.utcnow)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    pesquisa_id = db.Column(db.Integer, db.ForeignKey('pesquisas.id'), nullable=False)

    def __repr__(self):
        return f'<Resposta {self.id} - Nota {self.nota}>'
