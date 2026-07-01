import hashlib
from conexion import ConexionBD

def crear_usuario_admin():
    conexion = ConexionBD().obtener_conexion()
    cursor = conexion.cursor()
    
    usuario = "admin"
    password_plana = "inacap123" # La contraseña que usarás para entrar
    
    # ¡Aquí están los puntos de la rúbrica! Encriptación SHA-256
    password_hash = hashlib.sha256(password_plana.encode('utf-8')).hexdigest()
    
    sql = "INSERT INTO Usuario (username, password, rol) VALUES (%s, %s, %s)"
    valores = (usuario, password_hash, "Administrador")
    
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        print("¡Usuario administrador creado con éxito!")
    except Exception as e:
        print(f"Error al crear usuario: {e}")

if __name__ == "__main__":
    crear_usuario_admin()