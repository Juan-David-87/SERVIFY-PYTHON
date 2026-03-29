<?php
$host = "localhost";
$usuario = "root";
$contrasena = ""; // en WAMP normalmente está vacía
$base_datos = "servify";

$conn = new mysqli($host, $usuario, $contrasena, $base_datos);

if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

echo "Conexión exitosa";
?>