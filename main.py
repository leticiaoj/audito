from flask import Flask, render_template, redirect, request, flash
import json
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LET'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado:
        with open('usuarios.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
        return render_template("administrador.html", usuarios=usuarios)
    else:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    # Correção: colocar 'usuarios.json' entre aspas
    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        for usuario in usuarios:
            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')
            
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template("usuarios.html")
        
        # Se nenhum usuário for encontrado, exibe mensagem
        flash('Usuário inválido.')
        return redirect("/")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = {"nome": nome, "senha": senha}
    
    # Leitura do arquivo JSON
    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

    # Adicionar novo usuário
    usuarios.append(user)

    # Escrever no arquivo JSON
    with open('usuarios.json', 'w') as gravarTemp:
        json.dump(usuarios, gravarTemp, indent=4)
    
    logado = True
    flash(f'Cadastro de {nome} efetuado!')
    return redirect('/adm')

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('UsuarioPexcluir')
    usuarioDict = ast.literal_eval(usuario)
    nome = usuarioDict['nome']
    
    # Leitura e exclusão de usuário do JSON
    with open('usuarios.json') as usuariosTemp:
        usuariosJson = json.load(usuariosTemp)
        usuariosJson = [u for u in usuariosJson if u != usuarioDict]

    # Reescrever o arquivo JSON atualizado
    with open('usuarios.json', 'w') as usuarioAexcluir:
        json.dump(usuariosJson, usuarioAexcluir, indent=4)

    flash(f'Exclusão de {nome} realizada.')
    return redirect('/adm')

if __name__ == "__main__":
    app.run(debug=True)
