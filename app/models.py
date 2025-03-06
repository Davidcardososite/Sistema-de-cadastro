from .extensions import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rg = db.Column(db.String(150), unique=True, nullable=False) # precisa ser único
    cpf = db.Column(db.String(150), unique=True, nullable=False) # precisa ser único
    nome = db.Column(db.String(150), nullable=True) # Não precisa ser único
    sobrenome = db.Column(db.String(150), nullable=True)  # Não precisa ser único
    telefone = db.Column(db.String(150), unique=True, nullable=False) # precisa ser único
    rua = db.Column(db.String(150), nullable=True) # Não precisa ser único
    numero = db.Column(db.String(150), nullable=True) # Não precisa ser único
    bairro = db.Column(db.String(150), nullable=True) # Não precisa ser único
    vendas = db.relationship('Venda', back_populates='cliente', cascade='all, delete-orphan')

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(150), nullable=True) # Não precisa ser único
    tipo = db.Column(db.String(150), nullable=True) # Não precisa ser único
    valor = db.Column(db.Float, nullable=True)  # Valor deve ser numérico
    estoque = db.Column(db.Integer, nullable=True)  # Estoque não deve ser único
    vendas = db.relationship('Venda', back_populates='produto', cascade='all, delete-orphan')

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete='CASCADE'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id', ondelete='CASCADE'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=True)  # Quantidade deve ser numérica
    data_compra = db.Column(db.DateTime, nullable=True)
    cliente = db.relationship('Cliente', back_populates='vendas')
    produto = db.relationship('Produto', back_populates='vendas')




    


