from flask import Blueprint, current_app, jsonify, render_template, redirect, send_file, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
from db_config import create_connection
from app import app
from models import User
import requests

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

            if user and check_password_hash(user[2], password):
                login_user(User(user[0]))
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

    current_user_id = int(session.get('_user_id'))
    if not current_user_id:
        return jsonify(error="Usuário não autenticado."), 403
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT book_id, title, author, whatsapp, book_type, cover_url, description, user_id FROM book")
        books = cursor.fetchall()
        for book in books:
            book['current_user'] = current_user_id
    except Exception as e:
        print(f"Erro ao carregar os livros: {e}")
        flash(f"Erro ao carregar os livros: {e}")
        books = []
    finally:
        cursor.close()
        connection.close()
    return render_template('home.html', books=books)


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
            cursor.execute("SELECT email FROM user WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Email já cadastrado. Tente outro.")
                return render_template('register.html')

            hashed_password = generate_password_hash(password)

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




@routes.route('/add_book', methods=['POST'])
@login_required
def add_book():

    current_user_id = int(session.get('_user_id'))
    if not current_user_id:
        return jsonify(error="Usuário não autenticado."), 403
    
    title = request.form.get('bookTitle')
    author = request.form.get('bookAuthor')
    whatsapp = request.form.get('whatsapp')
    book_type = request.form.get('bookType')
    cover_url = request.form.get('coverUrl')
    description = request.form.get('description')


    if not title or not author or not whatsapp or not book_type:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO book (title, author, whatsapp, book_type, cover_url, description, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, author, whatsapp, book_type, cover_url, description, current_user_id))
        connection.commit()
        return jsonify({"success": "Livro adicionado com sucesso!"}), 200
    except Exception as e:
        connection.rollback()
        print("Erro ao adicionar ao banco:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()



@app.route('/delete_book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):

    current_user_id = int(session.get('_user_id'))
    if not current_user_id:
        return jsonify(error="Usuário não autenticado."), 403

    conn = create_connection()
    cursor = conn.cursor(dictionary=True) 
    try:
        cursor.execute("SELECT * FROM book WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()
        print(book)

        if book and book['user_id'] == current_user_id:
            cursor.execute("DELETE FROM book WHERE book_id = %s", (book_id,))
            conn.commit()
            return jsonify({'success': 'Livro excluído com sucesso!'}), 200
        else:
            return jsonify({'error': 'Ação não permitida!'}), 403
    except Exception as e:
        conn.rollback()
        print("Erro ao excluir do banco:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
