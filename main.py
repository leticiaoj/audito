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
    if logado == True:
        with open('usuarios.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)

        return render_template("administrador.html",usuarios=usuarios)
    if logado == False:
        return redirect('/')

@app.route ('/login', methods=['POST'])
def login ():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open(usuarios.json) as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        cont = 0
        for usuario in usuarios:
            cont += 1

            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')
            
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template("usuarios.html")
            
            if cont >= len(usuarios):
                flash('usuário inválido.')
                return redirect ("/")
            
@app.route('/cadastrarUsuario', methods = ['POST'])
def cadastrarUsuario ():
    global logado
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {
            "nome": nome,
            "senha": senha
        }
    ]
    with open ('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

    usuarioNovo = usuarios + user

    with open('usuarios.json', 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4)
        logado = True
        flash (F'cadastro de {nome} efetuado!')
        return redirect ('/adm')
    
@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('UsuarioPexcluir')
    usuarioDict = ast.literal_eval(usuario)
    nome = usuarioDict['nome']
    with open('usuarios.json') as usuariosTemp:
        usuariosJson = json.load(usuariosTemp)
        for c in usuariosJson:
            if c == usuarioDict:
                usuariosJson.remove(usuarioDict) 
                with open('usuarios.json', 'w') as usuarioAexcluir:
                    json.dump(usuariosJson, usuarioAexcluir, indent=4)
    flash(F'exclusão de {nome} realizada.')
    return redirect ('/adm')












if __name__ in "__main__":
    app.run(debug=True)