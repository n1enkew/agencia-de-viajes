import mysql.connector
from mysql.connector import Error

class ConexionBD:
    # Variable de clase para guardar la única instancia
    _instancia = None

    # El método __new__ es el corazón del Singleton
    def __new__(cls):
        if cls._instancia is None:
            # Si no existe la instancia, la crea
            cls._instancia = super(ConexionBD, cls).__new__(cls)
            cls._instancia.conexion = None
            cls._instancia._conectar()
        return cls._instancia

    def _conectar(self):
        try:
            # Reemplaza con tus datos de MySQL Workbench
            self.conexion = mysql.connector.connect(
                host='localhost',
                database='agencia', # El nombre de tu esquema en Workbench
                user='root',
                password='123456' # Pon tu clave de MySQL aquí (si tienes)
            )
            if self.conexion.is_connected():
                print("¡Conexión exitosa a la base de datos!")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")

    def obtener_conexion(self):
        return self.conexion

# Bloque de prueba: Si ejecutas este archivo directamente, probará la conexión
if __name__ == "__main__":
    # Creamos la instancia para probar
    bd = ConexionBD()