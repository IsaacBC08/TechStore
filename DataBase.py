import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

class Base_De_Datos:
    def __init__(self):
        """
        Constructor de la clase DB.
        Obtiene los datos de conexión desde un archivo .env.
        """
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()

        # Leer las variables de entorno
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.port = int(os.getenv('DB_PORT'))

        self.connection = None

    def iniciar_conexion(self):
        """
        Inicia la conexión a la base de datos.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port  # Agregamos el puerto
            )
            if self.connection.is_connected():
                print(f"Conexión a la base de datos '{self.database}' en {self.host}:{self.port}")
        except Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None
        return self.connection

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada exitosamente")

    def get_categories(self) -> list[dict]:
        """Retorna las categorías actuales de la DB"""
        conexion = self.iniciar_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT DISTINCT Categoría FROM Productos')
        categories = cursor.fetchall()
        cursor.close()
        self.cerrar_conexion()
        return categories
    
    def get_products(self, limit: int = 0, id=0, category: int =0, exclude:int =0) -> list[dict]:
        """Retorna los productos"""
        conexion = self.iniciar_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = 'SELECT * FROM Productos'
        conditions = []
        if id:
            conditions.append(f"Id_Producto = {id}")
        if category:
            conditions.append(f"Categoría = '{category}'")
        if exclude:
            conditions.append(f"Id_Producto != {exclude}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)  # Combina las condiciones con AND
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        products = cursor.fetchall()
        self.cerrar_conexion()
        return products