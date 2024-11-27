import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from models import Producto, Categoria,Tipo
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
        self.products_data = None
        self.categories = None

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
        cursor.execute('SELECT * FROM Categorias')
        categories = cursor.fetchall()
        cursor.close()
        print(categories)
        categories = [Categoria.crear_desde_registro(fila) for fila in categories]
        self.cerrar_conexion()
        return categories

    def get_types(self): 
        conexion = self.iniciar_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = '''
        SELECT 
            Tipos.*,
            Categorias.Nombre_Categoria AS categoria
        FROM
            Tipos
        JOIN 
            Categorias ON Tipos.Id_Categoria = Categorias.Id_Categoria
        '''
        cursor.execute(query)
        tipos = cursor.fetchall()
        tipos = [Tipo.crear_desde_registro(fila) for fila in tipos]
        cursor.close()
        return tipos

    def get_products_from_db(self):
        conexion = self.iniciar_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = '''
            SELECT 
                Productos.*, 
                Categorias.Nombre_Categoria AS Categoría,
                Tipos.Nombre_Tipo AS Tipo
            FROM 
                Productos
            JOIN 
                Categorias ON Productos.Id_Categoria = Categorias.Id_Categoria
            JOIN 
                Tipos ON Productos.Id_Tipo = Tipos.Id_Tipo;

        '''
        cursor.execute(query)
        self.products_data = cursor.fetchall()
        return


    def get_conditional_products(self, limit: int = 0, id=0, category: int =0, exclude:int =0, type:str=0) -> list[dict]:
        """Retorna los productos que cumplan con las condiciones pasadas"""
        if not self.products_data:
            self.get_products_from_db()

        # Filtrado de productos en memoria
        filtered_products = self.products_data

        if id:
            filtered_products = [prod for prod in filtered_products if prod['Id_Producto'] == id]
        if category:
            filtered_products = [prod for prod in filtered_products if prod['Categoría'] == category]
        if type:
            filtered_products = [prod for prod in filtered_products if prod['Tipo'] == type]
        if exclude:
            filtered_products = [prod for prod in filtered_products if prod['Id_Producto'] != exclude]

        if limit:
            filtered_products = filtered_products[:limit]

        return [Producto.crear_desde_registro(fila) for fila in filtered_products]
    
if __name__ == '__main__':
    db = Base_De_Datos()
    productos = db.get_categories()
    print(productos)