import sys
import hashlib
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from conexion import ConexionBD

class AgenciaViajes(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Cargar el diseño de Qt Designer
        loader = QUiLoader()
        archivo_ui = QFile("main.ui")
        archivo_ui.open(QFile.ReadOnly)
        self.ui = loader.load(archivo_ui, self)
        archivo_ui.close()
        
        # 2. Configurar la vista inicial (Mostrar página de Login)
        self.ui.stackedWidget.setCurrentIndex(0)
        
        # 3. Conectar el botón de login a nuestra función
        self.ui.btn_login.clicked.connect(self.verificar_login)
        
        self.ui.btn_agregar_destino.clicked.connect(self.agregar_destino)
        self.ui.btn_eliminar_destino.clicked.connect(self.eliminar_destino)

        self.cargar_destinos()


    def verificar_login(self):
        # Obtener los textos de los QLineEdit
        usuario = self.ui.txt_usuario.text()
        password = self.ui.txt_password.text()
        
        # Hashear la contraseña que ingresó el usuario
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        # Conectar a BD y verificar
        conexion = ConexionBD().obtener_conexion()
        cursor = conexion.cursor(dictionary=True) # dictionary=True para poder acceder por nombre de columna
        
        sql = "SELECT * FROM Usuario WHERE username = %s AND password = %s"
        cursor.execute(sql, (usuario, password))
        resultado = cursor.fetchone()
        
        if resultado:
            # Login exitoso: Cambiar a la página del Dashboard (Índice 1)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.txt_usuario.clear()
            self.ui.txt_password.clear()
        else:
            # Login fallido: Mostrar mensaje de error
            self.ui.lbl_mensaje.setText("Usuario o contraseña incorrectos")
            self.ui.lbl_mensaje.setStyleSheet("color: red;")
    
    def cargar_destinos(self):
        """Lee los destinos de la BD y los muestra en el QTableWidget"""
        # Limpiamos la tabla antes de cargar
        self.ui.tabla_destinos.setRowCount(0) 
        
        conexion = ConexionBD().obtener_conexion()
        cursor = conexion.cursor(buffered=True)
        
        try:
            cursor.execute("SELECT idDestino, nombre, costo FROM Destino")
            resultados = cursor.fetchall()
            
            from PySide6.QtWidgets import QTableWidgetItem
            
            for fila_num, fila_datos in enumerate(resultados):
                self.ui.tabla_destinos.insertRow(fila_num)
                # Convertimos cada dato a string para meterlo en la tabla
                self.ui.tabla_destinos.setItem(fila_num, 0, QTableWidgetItem(str(fila_datos[0])))
                self.ui.tabla_destinos.setItem(fila_num, 1, QTableWidgetItem(str(fila_datos[1])))
                self.ui.tabla_destinos.setItem(fila_num, 2, QTableWidgetItem(str(fila_datos[2])))
        except Exception as e:
            print(f"Error al cargar destinos: {e}")

    def agregar_destino(self):
        """Inserta un nuevo destino en la BD"""
        nombre = self.ui.txt_nombre_destino.text()
        costo = self.ui.txt_costo_destino.text()
        
        if not nombre or not costo:
            print("Faltan datos")
            return
            
        conexion = ConexionBD().obtener_conexion()
        cursor = conexion.cursor(buffered=True)
        
        try:
            sql = "INSERT INTO Destino (nombre, costo) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, int(costo)))
            conexion.commit()
            
            # Limpiamos los campos y recargamos la tabla
            self.ui.txt_nombre_destino.clear()
            self.ui.txt_costo_destino.clear()
            self.cargar_destinos()
        except Exception as e:
            print(f"Error al agregar destino: {e}")

    def eliminar_destino(self):
        """Elimina el destino seleccionado en la tabla"""
        fila_seleccionada = self.ui.tabla_destinos.currentRow()
        
        if fila_seleccionada == -1:
            print("Selecciona un destino para eliminar")
            return
            
        # Obtenemos el ID de la primera columna (columna 0)
        id_destino = self.ui.tabla_destinos.item(fila_seleccionada, 0).text()
        
        conexion = ConexionBD().obtener_conexion()
        cursor = conexion.cursor(buffered=True)
        
        try:
            sql = "DELETE FROM Destino WHERE idDestino = %s"
            cursor.execute(sql, (id_destino,))
            conexion.commit()
            
            self.cargar_destinos()
        except Exception as e:
            print(f"Error al eliminar destino: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = AgenciaViajes()
    ventana.ui.show()
    sys.exit(app.exec())