from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta principal - Página de inicio de SERVIFY
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para registro de usuarios en SERVIFY
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        tipo_usuario = request.form.get('tipo_usuario')  # Cliente o Proveedor
        
        return render_template('register.html', 
                             registrado=True, 
                             nombre=nombre,
                             email=email,
                             tipo_usuario=tipo_usuario)
    
    return render_template('register.html', registrado=False)

# Ruta para inicio de sesión en SERVIFY
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        recordar = request.form.get('recordar')  # Checkbox "Recordarme"
        
        # Simulación: cualquier email con @ es "válido"
        if '@' in email:
            return render_template('login.html', 
                                 logeado=True, 
                                 email=email,
                                 recordar=recordar)
        else:
            return render_template('login.html', error=True)
    
    return render_template('login.html', logeado=False)

# Ruta para recuperar contraseña en SERVIFY
@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        email = request.form.get('email')
        return render_template('recover.html', enviado=True, email=email)
    
    return render_template('recover.html', enviado=False)

# Ruta para perfil de usuario en SERVIFY
@app.route('/profile')
def profile():
    # Datos simulados de un usuario de SERVIFY
    usuario = {
        'nombre': 'Carlos Rodríguez',
        'email': 'carlos@servify.co',
        'tipo': 'Cliente',  # Puede ser 'Cliente' o 'Proveedor'
        'miembro_desde': 'Abril 2026',
        'servicios_contratados': 7,
        'servicios_ofrecidos': 4,
        'calificacion': '4.7 ⭐',
        'telefono': '+57 300 987 6543',
        'ciudad': 'Bogotá',
        'documento': 'CC 123456789'
    }
    return render_template('profile.html', usuario=usuario)

# Ejecutar la aplicación como simulación de flask del proyecto 
if __name__ == '__main__':
    app.run(debug=True)