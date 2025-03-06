# funcoes.py
import re
from .extensions import db
from .models import Cliente, Produto, Venda


def inserir_cliente(rg, cpf, nome, sobrenome, telefone, rua, numero, bairro):
    cliente = Cliente(
        rg=rg,
        cpf=cpf,
        nome=nome,
        sobrenome=sobrenome,
        telefone=telefone,
        rua=rua,
        numero=numero,
        bairro=bairro
    )
    db.session.add(cliente)
    db.session.commit()
    return cliente.id





def inserir_produto(produto, tipo, valor, estoque):
    produto_obj = Produto(
        produto=produto,
        tipo=tipo,
        valor=valor,
        estoque=estoque
    )
    db.session.add(produto_obj)
    db.session.commit()
    return produto_obj.id





def inserir_venda(id_cliente, id_produto, quantidade, data_compra):
    venda = Venda(
        id_cliente=id_cliente,
        id_produto=id_produto,
        quantidade=quantidade,
        data_compra=data_compra
    )
    db.session.add(venda)
    db.session.commit()



def pesquisar_cliente(nome):
    nome = f"%{nome.strip().lower()}%"
    clientes = Cliente.query.filter(Cliente.nome.ilike(nome)).all()
    return clientes




def pesquisar_produto_por_cliente(cliente_id):
    vendas = Venda.query.filter_by(id_cliente=cliente_id).all()
    produtos = [venda.produto for venda in vendas]
    return produtos


def pesquisar_venda_por_cliente(cliente_id):
    vendas = Venda.query.filter_by(id_cliente=cliente_id).all()
    return vendas

    
    
    
def atualizar_cliente(id, rg, cpf, nome, sobrenome, telefone, rua, numero, bairro):
    cliente = Cliente.query.get(id)
    if cliente:
        cliente.rg = rg
        cliente.cpf = cpf
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.telefone = telefone
        cliente.rua = rua
        cliente.numero = numero
        cliente.bairro = bairro
        db.session.commit()


def deletar_cliente_por_id(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()



def atualizar_produto(id, produto, tipo, valor, estoque):
    produto_obj = Produto.query.get(id)
    if produto_obj:
        produto_obj.produto = produto
        produto_obj.tipo = tipo
        produto_obj.valor = valor
        produto_obj.estoque = estoque
        db.session.commit()



def atualizar_venda(id, quantidade):
    venda = Venda.query.get(id)
    if venda:
        venda.quantidade = quantidade
        db.session.commit()



def pesquisar_cliente_por_id(id):
    cliente = Cliente.query.get(id)
    return cliente


def pesquisar_produto_por_id(id):
    produto = Produto.query.get(id)
    return produto


def pesquisar_venda_por_id(id):
    venda = Venda.query.get(id)
    return venda

    
    
    
    
    
# função validação do cpf
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])
    
    
    
# função validação do rg
def validar_rg(rg):
    rg = re.sub(r'\W', '', rg)
    if len(rg) < 7 or len(rg) > 9:
        return False
    if not re.match(r'^[0-9A-Za-z]+$', rg):
        return False
    return True