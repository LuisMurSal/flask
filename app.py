from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_session import Session
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)

# Configuración de Flask-Session
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SECRET_KEY'] = 'secret_key_example'
Session(app)

# Base de datos
users = {
    "boly": hashpw(b"limones", gensalt()),  # Usuario y contraseña actualizados
}

@app.route('/')
def index():
    if 'username' in session:
        return f'¡Hola {session["username"]}! Ya has iniciado sesión. <a href="/logout">Cerrar sesión</a>'
    return 'No has iniciado sesión. <a href="/login">Iniciar sesión</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if username in users and checkpw(password, users[username]):
            session['username'] = username
            flash(f'¡Bienvenido {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'username' in session:
        return f'Esta es una ruta protegida. ¡Hola {session["username"]}!'
    else:
        flash('Necesitas iniciar sesión para acceder a esta página.', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
