from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import create_user, create_worker_service, get_all_services, get_user_by_email, get_user_by_id, get_services_by_worker

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
        phone = request.form["phone"]
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
        create_user(name, email, phone, password_hash, tipo_usuario)

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
            session["user_id"] = user["id"]
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

    servicios = []

    if session["role"] == "worker":
        servicios = get_services_by_worker(session["user_id"])

    user = get_user_by_id(session["user_id"])

    usuario = {
    'nombre': user["name"],
    'email': user["email"],
    'tipo': user["role"],
    'servicios_ofrecidos': len(servicios)
    }

    return render_template('profile.html', usuario=usuario, servicios=servicios)

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

@app.route('/my-services', methods=['GET', 'POST'])
def my_services():
    if "user_id" not in session:
        return redirect('/login')

    user = get_user_by_id(session["user_id"])

    if not user:
        return redirect('/login')

    if user.get("role") != "worker":
        return "Acceso denegado"

    if request.method == 'POST':
        service_id = request.form.get("service_id")
        price = request.form.get("price")

        if not service_id or not price:
            return "Datos incompletos"

        create_worker_service(session["user_id"], service_id, price)

    services = get_all_services()

    return render_template("servicios.html", services=services)

# ▶️ RUN
if __name__ == '__main__':
    app.run(debug=True)