from flask import Flask, render_template, request, redirect
import psycopg2
import os

# Configurações do banco de dados usando variáveis de ambiente
DB_NAME = os.environ.get("DB_NAME", "sua_base")
DB_USER = os.environ.get("DB_USER", "seu_usuario")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "sua_senha")
DB_HOST = os.environ.get("DB_HOST", "seu-endpoint-rds")

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if name and email:
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    # Para produção, use gunicorn; este é apenas para testes locais
    app.run(host='0.0.0.0', port=5000, debug=True)
