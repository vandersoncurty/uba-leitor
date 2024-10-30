from flask import Blueprint, current_app, jsonify, render_template, redirect, send_file, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
from db_config import create_connection
from app import app
from models import User

# Instância do Blueprint
routes = Blueprint('routes', __name__)

@app.route('/')
def index():
    return redirect(url_for('routes.home'))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = create_connection()
        if not connection:
            flash("Erro ao conectar ao banco de dados")
            return render_template('login.html')

        cursor = connection.cursor()
        try:
            cursor.execute("""SELECT user_id, email, password FROM user WHERE email = %s""", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):  # Índice 2 para a senha
                login_user(User(user[0]))  # Índice 0 para o ID do usuário
                return redirect(url_for('routes.home'))
            else:
                flash('Email ou senha incorretos')
        except Exception as e:
            flash(f"Erro ao realizar login: {e}")
        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')

@routes.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        password = request.form['password']

        connection = create_connection()
        if not connection:
            flash("Erro ao conectar ao banco de dados")
            return render_template('register.html')

        cursor = connection.cursor()
        try:
            # Verificar se o email já está cadastrado
            cursor.execute("SELECT email FROM user WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Email já cadastrado. Tente outro.")
                return render_template('register.html')

            # Gerar o hash da senha
            hashed_password = generate_password_hash(password)

            # Inserindo o novo usuário na tabela
            cursor.execute("""INSERT INTO user (name, phone, email, password) 
                              VALUES (%s, %s, %s, %s)""",
                           (nome, telefone, email, hashed_password))
            connection.commit()
            flash("Registro realizado com sucesso! Você pode fazer login agora.")
            return redirect(url_for('routes.login'))
        except Exception as e:
            flash(f"Erro ao registrar: {e}")
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')