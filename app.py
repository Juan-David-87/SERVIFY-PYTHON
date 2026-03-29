from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'hospital_secret_key_2024'  # Cámbiala por algo más seguro

# ── Configuración de MySQL ───────────────────────────────────────────────────
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',        # Cambia por tu usuario de MySQL
        password='',        # Cambia por tu contraseña de MySQL
        database='servify'
    )

# ── Ruta principal ───────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

# ── Registro ─────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre       = request.form.get('nombre')
        email        = request.form.get('email')
        tipo_usuario = request.form.get('tipo_usuario')

        return render_template('register.html',
                               registrado=True,
                               nombre=nombre,
                               email=email,
                               tipo_usuario=tipo_usuario)

    return render_template('register.html', registrado=False)

# ── Login con MySQL ──────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya hay sesión activa, redirigir al perfil
    if 'usuario' in session:
        return redirect(url_for('profile'))

    error = False

    if request.method == 'POST':
        email      = request.form.get('email', '').strip()
        contrasena = request.form.get('contrasena', '').strip()

        try:
            conn   = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_Usuario, nombre, email, contrasena FROM usuarios WHERE email = %s",
                (email,)
            )
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()

            # Comparación en texto plano (solo para pruebas)
            # Cuando uses hash reemplaza por: check_password_hash(usuario['contrasena'], contrasena)
            print("Usuario encontrado:", usuario)
            print("Contraseña ingresada:", contrasena)
            if usuario and contrasena == usuario['contrasena']:
                session['usuario'] = usuario['id_Usuario']
                session['nombre']  = usuario['nombre']
                session['email']   = usuario['email']
                return redirect(url_for('profile'))
            else:
                error = True

        except Exception as e:
            print('Error de BD:', e)
            error = True

    return render_template('login/login.html', error=error, logeado=False)

# ── Cerrar sesión ─────────────────────────────────────────────────────────────
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('login'))

# ── Recuperar contraseña ──────────────────────────────────────────────────────
@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        email = request.form.get('email')
        return render_template('recover.html', enviado=True, email=email)

    return render_template('recover.html', enviado=False)

# ── Perfil ────────────────────────────────────────────────────────────────────
@app.route('/profile')
def profile():
    # Si hay sesión activa, usar datos reales
    if 'usuario' in session:
        usuario = {
            'nombre':                session['nombre'],
            'email':                 session['email'],
            'tipo':                  'Usuario',
            'miembro_desde':         'Marzo 2026',
            'servicios_contratados': 0,
            'servicios_ofrecidos':   0,
            'calificacion':          'N/A',
            'telefono':              'N/A',
            'ciudad':                'N/A',
            'documento':             'N/A'
        }
    else:
        # Datos simulados si no hay sesión (igual que antes)
        usuario = {
            'nombre':                'Carlos Rodríguez',
            'email':                 'carlos@servify.co',
            'tipo':                  'Cliente',
            'miembro_desde':         'Marzo 2026',
            'servicios_contratados': 5,
            'servicios_ofrecidos':   0,
            'calificacion':          '4.8 ⭐',
            'telefono':              '+57 300 987 6543',
            'ciudad':                'Bogotá',
            'documento':             'CC 123456789'
        }

    return render_template('profile.html', usuario=usuario)

# ── Ejecutar ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)