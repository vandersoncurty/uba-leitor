import os
from flask import Flask
from flask_login import LoginManager
from mysql.connector import connect, Error  # Altere para o conector MySQL
from db_config import create_connection, close_connection
from models import User
from app import app, login_manager

# Certifique-se de que os diretórios de upload e download existam
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

@login_manager.user_loader
def load_user(user_id):
    connection = create_connection()
    try:
        cursor = connection.cursor(dictionary=True)  # Use 'dictionary=True' para retornar dicionários
        cursor.execute("SELECT user_id FROM user WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
    except Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        user = None
    finally:
        cursor.close()
        connection.close()
        
    if user:
        return User(user['user_id'])  # Acesse o ID do usuário no dicionário
    return None

# Importa e registra as rotas a partir do Blueprint
from routes import routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
