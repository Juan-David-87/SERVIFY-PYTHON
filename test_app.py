import unittest
from app import app  # Importamos tu aplicación Flask

class TestRutasBasicasSERVIFY(unittest.TestCase):
    """
    Suite de pruebas para verificar el acceso básico a las rutas de la aplicación.
    """
    def setUp(self):
        # Configuramos la aplicación en modo de pruebas
        app.config['TESTING'] = True
        # Creamos un cliente de pruebas
        self.client = app.test_client()

    def test_ruta_home(self):
        # Hacemos una petición GET a la ruta principal
        respuesta = self.client.get('/')
        # Verificamos que el código de estado sea 200 (OK)
        self.assertEqual(respuesta.status_code, 200)
        # Verificamos que el contenido HTML incluya el nombre del proyecto
        self.assertIn(b'SERVIFY', respuesta.data)

    def test_ruta_perfil(self):
        # Verificamos la ruta de perfil simulada
        respuesta = self.client.get('/profile')
        self.assertEqual(respuesta.status_code, 200)
        # Validamos que los datos simulados de Carlos Rodríguez estén presentes
        self.assertIn(b'Carlos', respuesta.data)
        self.assertIn(b'Cliente', respuesta.data)

class TestFuncionalidadFormularios(unittest.TestCase):
    """
    Suite de pruebas para evaluar la lógica y el manejo de datos en los formularios (POST).
    """
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_registro_exitoso_simulado(self):
        # Simulamos el envío de datos a través del formulario de registro
        datos_registro = {
            'nombre': 'Estudiante Prueba',
            'email': 'estudiante@servify.co',
            'tipo_usuario': 'Proveedor'
        }
        respuesta = self.client.post('/register', data=datos_registro)
        self.assertEqual(respuesta.status_code, 200)
        # Validamos que la plantilla renderice el mensaje de éxito
        self.assertIn(b'Registro exitoso', respuesta.data)
        self.assertIn(b'Estudiante Prueba', respuesta.data)

    def test_login_email_valido(self):
        # En la lógica de tu app, cualquier email con '@' es válido
        datos_login = {
            'email': 'usuario@servify.co',
            'password': 'password123'
        }
        respuesta = self.client.post('/login', data=datos_login)
        self.assertEqual(respuesta.status_code, 200)
        # assertTrue podría usarse en la lógica interna, aquí verificamos la vista
        self.assertIn(b'Sesion iniciada', respuesta.data.replace(b'\xc3\xb3', b'o')) # Manejo de tildes en bytes

    def test_login_email_invalido(self):
        # Verificamos el manejo de errores: un email sin '@' debe fallar
        datos_login = {
            'email': 'usuario_sin_arroba',
            'password': 'password123'
        }
        respuesta = self.client.post('/login', data=datos_login)
        self.assertEqual(respuesta.status_code, 200)
        # El sistema debe detectar la credencial inválida
        self.assertIn(b'Credenciales', respuesta.data)

if __name__ == '__main__':
    # Ejecuta todas las pruebas cuando se corre el script directamente
    unittest.main(verbosity=2)