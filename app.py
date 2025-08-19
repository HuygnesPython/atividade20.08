from flask import Flask, redirect, request, url_for, render_template
import bcrypt as b
import mysql.connector as my
app = Flask(__name__)
def conectar_banco():
    conexao = my.connect(
        host = 'localhost',
        user = 'root',
        password = 'neto2303',
        database = 'loja'
    )
    return conexao



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastrar', methods=['GET','POST'])
def cadastro():

    if request.method == 'GET':
        return render_template('cadastro.html')
    
    if request.method == 'POST':

        nome = request.form.get('nome')
        senha = request.form.get('senha')
        senha_crypt = b.hashpw(senha.encode(), salt=b.gensalt())

        conexao = conectar_banco()
        cursor = conexao.cursor()
        sql = f"insert into clientes (nome, senha) values ('{nome}', '{senha}')"
        cursor.execute(sql)
        conexao.commit()
        conexao.close()

        
        return render_template('cadastrado.html', nome = nome, senha = senha, senha_crypt = senha_crypt)

@app.route('/entrar', methods=['GET','POST'])
def entrar():

    if request.method == 'GET':
        return render_template('entrar.html')
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        sql = f"select * from clientes"
        cursor.execute(sql)
        clientes = cursor.fetchall()
        conexao.close()
        for cliente in clientes:

            if cliente['nome'] == nome:

                if cliente['senha'] == senha:
                    
                    print(nome, 'entrou')
                    return render_template('entrou.html', nome = nome, senha = senha)
        return render_template('naoentrou.html')       
        
@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

@app.route('/imc', methods=['GET', 'POST'])
def imc():
    if request.method == 'GET':
        return render_template('imc.html')
    
    if request.method == 'POST':
        peso = float(request.form.get('peso'))
        altura = float(request.form.get('alt'))
        imc = peso / (altura ** 2)
        return render_template('ImcCalculado.html', imc=imc)

app.run(debug=True)