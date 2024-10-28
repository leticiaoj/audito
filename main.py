from flask import Flask, render_template, redirect, request, flash, send_from_directory
import json
import ast
import os

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


@app.route('/auditor')
def auditor():
    if logado == True:
      arquivo = []
      for documento in os.listdir('static/arquivos'):
        arquivo.append(documento)
      return render_template("auditor.html", arquivos=arquivo)
    else:
        return redirect('/')
    
@app.route('/usuarios')
def usuarios():
    if logado == True:
      return render_template("usuarios.html")
    else:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        for usuario in usuarios:
            if nome == 'admin01' and senha == 'administrador':
                logado = True
                return redirect('/adm')

            if nome == 'auditor01' and senha == 'auditoriando':
                logado = True
                return redirect('/auditor')
            
            if usuario['nome'] == nome and usuario['senha'] == senha:
                logado = True
                return render_template("usuarios.html")
        
        flash('usuário inválido.')
        return redirect("/")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = {"nome": nome, "senha": senha}

    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

    usuarios.append(user)

    with open('usuarios.json', 'w') as gravarTemp:
        json.dump(usuarios, gravarTemp, indent=4)
    
    logado = True
    flash(f'cadastro de {nome} efetuado!')
    return redirect('/adm')

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuarioPexcluir')
    usuarioDict = ast.literal_eval(usuario)
    nome = usuarioDict['nome']
    
    #with open('usuarios.json') as usuariosTemp:
    #    usuariosJson = json.load(usuariosTemp)
    #    usuariosJson = [u for u in usuariosJson if u != usuarioDict]

    with open('usuarios.json') as usuariosTemp:
        usuariosJson = json.load(usuariosTemp)
        for c in usuariosJson:
            if c == usuarioDict:
                usuariosJson.remove(usuarioDict)
                with open('usuarios.json', 'w') as usuarioAexcluir:
                  json.dump(usuariosJson, usuarioAexcluir, indent=4)

    flash(f'exclusão de {nome} realizada.')
    return redirect('/adm')


@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True

    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ", "-")
    arquivo.save(os.path.join('static/arquivos/', nome_arquivo))

    flash('arquivo enviado!')
    return redirect('/usuarios')

@app.route('/download', methods=['POST'])
def download():
    nomeArquivo = request.form.get('arquivosParaDownload')

    return send_from_directory('static/arquivos', nomeArquivo, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
