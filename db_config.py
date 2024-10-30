import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def create_connection():
    """Cria uma conexão ao banco de dados MySQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        if connection.is_connected():
            print("Conexão bem-sucedida ao banco de dados")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def close_connection(connection):
    """Fecha a conexão ao banco de dados MySQL."""
    if connection.is_connected():
        connection.close()
        print("Conexão ao banco de dados encerrada")
