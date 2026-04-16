from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "clave_secreta"

# 🏠 HOME
@app.route('/')
def home():
    return render_template('index.html')

# 📝 REGISTRO
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        tipo_usuario = request.form["tipo_usuario"]

        # 🔒 Validar contraseñas
        if password != confirm_password:
            return "Las contraseñas no coinciden"

        # 🚫 Evitar duplicados
        if get_user_by_email(email):
            return "El correo ya está registrado"

        # 🔐 Hash
        password_hash = generate_password_hash(password)

        # 💾 Guardar en BD
        create_user(name, email, password_hash, tipo_usuario)

        return render_template(
            "register.html",
            registrado=True,
            nombre=name,
            tipo_usuario=tipo_usuario,
            email=email
        )

    return render_template("register.html", registrado=False)

# 🔑 LOGIN REAL
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)

        if user and check_password_hash(user["password_hash"], password):
            # ✅ Guardar sesión
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]

            return redirect('/profile')
        else:
            return render_template('login.html', error=True)

    return render_template('login.html')

# 👤 PERFIL REAL (con sesión)
@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect('/login')

    usuario = {
        'nombre': session["user_name"],
        'email': 'No cargado aún',
        'tipo': session["role"]
    }

    return render_template('profile.html', usuario=usuario)

# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# 🔁 RECOVER (puedes mejorarlo después)
@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        email = request.form.get('email')
        return render_template('recover.html', enviado=True, email=email)

    return render_template('recover.html', enviado=False)

# ▶️ RUN
if __name__ == '__main__':
    app.run(debug=True)