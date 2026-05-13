from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import create_user, create_worker_service, delete_worker_service, get_all_services, get_user_by_email, get_user_by_id, get_services_by_worker

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

        if password != confirm_password:
            return "Las contraseñas no coinciden"

        if get_user_by_email(email):
            return "El correo ya está registrado"

        password_hash = generate_password_hash(password)
        create_user(name, email, phone, password_hash, tipo_usuario)

        return render_template(
            "register.html",
            registrado=True,
            nombre=name,
            tipo_usuario=tipo_usuario,
            email=email
        )

    return render_template("register.html", registrado=False)

# 🔑 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["nombre"] = user["name"]  # ← NUEVO: guarda el nombre en sesión

            return redirect('/cliente')
        else:
            return render_template('login.html', error=True)

    return render_template('login.html')

# 👤 PERFIL
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
        'telefono': user.get("phone"),
        'tipo': user["role"],
        'servicios_ofrecidos': len(servicios)
    }

    all_services = get_all_services()

    return render_template(
        'profile.html',
        usuario=usuario,
        servicios=servicios,
        all_services=all_services
    )

# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# 🔁 RECOVER
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

@app.route('/add-service', methods=['POST'])
def add_service():
    if "user_id" not in session:
        return redirect('/login')

    service_id = request.form.get("service_id")
    price = request.form.get("price")

    if not service_id or not price:
        return redirect('/profile')

    create_worker_service(session["user_id"], service_id, price)

    return redirect('/profile')

@app.route('/delete-service', methods=['POST'])
def delete_service():
    if "user_id" not in session:
        return redirect('/login')

    service_id = request.form.get("service_id")
    delete_worker_service(service_id, session["user_id"])

    return redirect('/profile')

# 🧑 CLIENTE DASHBOARD
@app.route('/cliente')
def cliente_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    servicios = get_all_services()                      # ← NUEVO: carga los servicios
    nombre = session.get("nombre", "Cliente")           # ← NUEVO: lee el nombre de sesión

    q = request.args.get('q', '').strip().lower()
    cat = request.args.get('cat', '').strip()

    if q:
        servicios = [s for s in servicios if q in s['nombre'].lower()]
    if cat:
        servicios = [s for s in servicios if s['tipo'] == cat]

    return render_template(
        'clientes/cliente_dashboard.html',
        servicios=servicios,
        nombre=nombre
    )

# ▶️ RUN
if __name__ == '__main__':
    app.run(debug=True)