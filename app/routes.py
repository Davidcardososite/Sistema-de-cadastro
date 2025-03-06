# routes.py
from datetime import datetime
import logging
from flask import Blueprint, session, render_template, redirect, url_for, flash, request
from .models import Cliente
from .funcoes import (
inserir_cliente,
inserir_produto,
inserir_venda,
pesquisar_cliente,
pesquisar_produto_por_cliente,
pesquisar_venda_por_cliente,
atualizar_cliente, atualizar_produto,
pesquisar_produto_por_id,
deletar_cliente_por_id,
pesquisar_venda_por_id,
atualizar_venda,
validar_rg,
validar_cpf
)

auth_bp = Blueprint('auth', __name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

# Rota para o dashboard do usuário logado
@auth_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@auth_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        rg = request.form['rg']
        cpf = request.form['cpf']
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        telefone = request.form['telefone']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']

        # Validação de CPF e RG
        if not validar_cpf(cpf):
            return render_template('cadastrar.html', msg="CPF inválido!")
        if not validar_rg(rg):
            return render_template('cadastrar.html', msg="RG inválido!")

        try:
            id_cliente = inserir_cliente(rg, cpf, nome, sobrenome, telefone, rua, numero, bairro)
            if id_cliente:
                return redirect(url_for('auth.produto', id_cliente=id_cliente))
            else:
                return render_template('cadastrar.html', msg="Erro ao cadastrar cliente!")
        except Exception as e:
            logging.error(f"Erro ao cadastrar cliente: {e}")
            return render_template('cadastrar.html', msg=f"Erro ao cadastrar: {e}")
    return render_template('cadastrar.html')






# função cadastrar produto
@auth_bp.route('/produto', methods=['GET', 'POST'])
def produto():
    id_produto = request.args.get('id_produto') or session.get('id_produto')
    
    id_cliente = request.args.get('id_cliente') or session.get('id_cliente')
    if not id_cliente:
        flash("Cliente não encontrado!", "error")
        return redirect(url_for('auth.cadastrar'))


    if request.method == 'POST':
        produto = request.form['produto']
        tipo = request.form['tipo']
        valor = request.form['valor']
        estoque = request.form['estoque']

        try:
            id_produto = inserir_produto(produto, tipo, valor, estoque)
            if id_produto:
                flash("Produto cadastrado com sucesso!", "success")
                return redirect(url_for('auth.venda', id_cliente=id_cliente, id_produto=id_produto))
            else:
                flash("Erro ao cadastrar produto.", "error")
                msg = "Erro ao cadastrar produto."
                return render_template('produto.html', id_cliente=id_cliente, msg=msg)
        except Exception as e:
            flash("Erro ao cadastrar produto: " + str(e), "error")
            msg = "Erro ao cadastrar: " + str(e)
            return render_template('produto.html', id_cliente=id_cliente, msg=msg)
    return render_template('produto.html', id_cliente=id_cliente)

    
    
    
    


# rota para a página venda
@auth_bp.route('/venda', methods=['GET', 'POST'])
def venda():
    id_produto = request.args.get('id_produto') or session.get('id_produto')
    id_cliente = request.args.get('id_cliente') or session.get('id_cliente')
    
    if request.method == 'POST':
        quantidade = request.form['quantidade']
        # formato da data
        data_compra = datetime.now()
        logging.info(f"data da compra: {data_compra}")

        try:
            inserir_venda(id_cliente, id_produto, quantidade, data_compra)
            msg = "Venda registrada com sucesso!"
            return render_template('venda.html', msg=msg)
        except Exception as e:
            msg = f"Erro ao registrar venda: {str(e)}"
            logging.error(f"Erro ao registrar venda: {e}")
            flash("Erro ao registrar venda. Verifique os dados!", "error")
            return render_template('venda.html', id_cliente=id_cliente, id_produto=id_produto, msg=msg)
    return render_template('venda.html', id_cliente=id_cliente, id_produto=id_produto)

    
    
    
    
# rota para a página pesquisar 
@auth_bp.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    resultados_cliente = []
    resultados_produto = {}
    resultados_venda = {}
    msg = None
    if request.method == 'POST':
        nome = request.form['nome']
        resultados_cliente = pesquisar_cliente(nome)
        if not resultados_cliente:
            msg = "Nenhum cliente encontrado."
        else:
            for cliente in resultados_cliente:
                cliente_id = cliente.id  # Acessa o atributo 'id' diretamente
                resultados_produto[cliente_id] = pesquisar_produto_por_cliente(cliente_id)
                resultados_venda[cliente_id] = pesquisar_venda_por_cliente(cliente_id)
    return render_template(
        'pesquisar.html',
        resultados_cliente=resultados_cliente,
        resultados_produto=resultados_produto,
        resultados_venda=resultados_venda,
        msg=msg
    )





# rota para deletar cliente
@auth_bp.route('/deletar_cliente/<int:id>', methods=['POST'])
def deletar_cliente(id):
    try:
        deletar_cliente_por_id(id)
        flash("Cliente deletado com sucesso!")
    except Exception as e:
        msg = "Erro ao deletar cliente: " + str(e)
        flash("Erro ao deletar: " + str(e))
    return redirect(url_for('auth.pesquisar'))





# rota para editar produto
@auth_bp.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if request.method == 'POST':
        produto = request.form['produto']
        tipo = request.form['tipo']
        preco = request.form['preco']
        estoque = request.form['estoque']
        
        try:
            atualizar_produto(id, produto, tipo, preco, estoque)
            flash("Produto atualizado com sucesso!")
            return redirect(url_for('auth.pesquisar'))
        except Exception as e:
            logging.error(f"Erro ao atualizar produto: {e}")
            flash("Erro ao atualizar produto. Verifique os dados!", "error")
            return redirect(url_for('auth.editar_produto', id=id))
    produto = pesquisar_produto_por_id(id)
    return render_template('editar_produto.html', produto=produto)




# rota para editar venda
@auth_bp.route('/editar_venda/<int:id>', methods=['GET', 'POST'])
def editar_venda(id):
    if request.method == 'POST':
        quantidade = request.form['quantidade']
        
        try:
            atualizar_venda(id, quantidade)
            flash("Venda atualizada com sucesso!")
            return redirect(url_for('auth.pesquisar'))
        except Exception as e:
            flash("Erro ao atualizar: " + str(e))
            return render_template('.editar_venda.html', id=id)
    venda = pesquisar_venda_por_id(id)
    return render_template('editar_venda.html', venda=venda)
    
    
    
# rota editar cliente
@auth_bp.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)  # Busca o cliente ou retorna 404

    if request.method == 'POST':
        # Obtendo dados do formulário
        rg = request.form['rg']
        cpf = request.form['cpf']
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        telefone = request.form['telefone']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']

        # Validação de dados
        if not validar_cpf(cpf):
            flash("CPF inválido. Por favor, digite novamente.", "error")
            return render_template('editar_cliente.html', cliente=cliente)

        if not validar_rg(rg):
            flash("RG inválido. Por favor, digite novamente.", "error")
            return render_template('editar_cliente.html', cliente=cliente)

        # Atualização do cliente
        try:
            atualizar_cliente(id, rg, cpf, nome, sobrenome, telefone, rua, numero, bairro)
            flash("Cliente atualizado com sucesso!", "success")
            return redirect(url_for('auth.pesquisar'))  # Ajuste o nome da rota se necessário
        except Exception as e:
            flash(f"Erro ao atualizar cliente: {e}", "error")
            return render_template('editar_cliente.html', cliente=cliente)

    # Renderiza o formulário com os dados do cliente
    return render_template('editar_cliente.html', cliente=cliente)
