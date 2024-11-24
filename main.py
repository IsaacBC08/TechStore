from flask import Flask, render_template, request, redirect, url_for, flash, current_app, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from uuid import uuid4
from DataBase import Base_De_Datos
from models import Producto
from dotenv import load_dotenv

app = Flask(__name__)
db = Base_De_Datos()
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

class Config:
    UPLOAD_FOLDER = 'static/uploads/productos'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

# Función para verificar las extensiones permitidas de las imágenes
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_unique_filename(filename):
    """Genera un nombre único para el archivo usando UUID y timestamp"""
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid4().hex}_{int(datetime.now().timestamp())}.{ext}"


@app.route('/')
def index():
    productos_data = db.get_products(limit=3) # solo queremos 3 productos
    productos = [Producto.crear_desde_registro(fila) for fila in productos_data]
    return render_template('index.html', productos=productos)

@app.route('/productos')
def productos():
    productos_data = db.get_products()
    categorias = db.get_categories()
    productos = [Producto.crear_desde_registro(fila) for fila in productos_data]
    db.cerrar_conexion()
    return render_template('productos.html', productos=productos,categorias=categorias)

@app.route('/detalles/<int:id>')
def detalles(id):
    producto = db.get_products(id=id)
    producto = Producto.crear_desde_registro(producto[0])
    relacionados = db.get_products(category=producto.categoria, limit=3, exclude=id)
    relacionados = [Producto.crear_desde_registro(fila) for fila in relacionados]
    return render_template('detalles.html', producto = producto, relacionados = relacionados)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form['Nombre_Producto']
            precio = request.form['Precio']
            descripcion = request.form['Descripcion']
            categoria = request.form['Categoria']
            estado = request.form['Estado']
            imagen = request.files.get('Imagen')
            
            # Validaciones

            if not imagen or not allowed_file(imagen.filename):
                flash('Formato de imagen no permitido', 'error')
                return redirect(request.url)

            imagen.seek(0)
            if len(imagen.read()) > Config.MAX_IMAGE_SIZE:
                flash('La imagen es demasiado grande. Máximo 5MB', 'error')
                return redirect(request.url)
            imagen.seek(0)

            # Guardar la imagen
            filename = get_unique_filename(secure_filename(imagen.filename))
            upload_path = os.path.join(current_app.root_path, Config.UPLOAD_FOLDER)
            os.makedirs(upload_path, exist_ok=True)
            imagen_path = os.path.join(upload_path, filename)
            imagen.save(imagen_path)
            imagen_url = f"{Config.UPLOAD_FOLDER}/{filename}"

            # Insertar en la base de datos
            conexion = db.iniciar_conexion()
            try:
                query = """INSERT INTO Productos (Nombre_Producto, Descripcion, Precio, Imagen,Categoria, Estado) 
                           VALUES (%s, %s, %s, %s)"""
                conexion.cursor().execute(query, (nombre, descripcion, precio, imagen_url, categoria, estado))
                conexion.commit()
                flash('Producto agregado exitosamente', 'success')
            except Exception as e:
                if os.path.exists(imagen_path):
                    os.remove(imagen_path)
                flash(f'Error al agregar producto: {str(e)}', 'error')
            finally:
                conexion.close()

            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Error al agregar producto: {str(e)}', 'error')
    
    return render_template('Add_Product.html')


if __name__ == "__main__":
    app.run(debug=True)