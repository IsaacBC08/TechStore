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
    return render_template('index.html')

@app.route('/productos/')
@app.route('/productos/<string:tipo>')
def productos(tipo=None):
    if tipo:
        productos_data = db.get_conditional_products(type=tipo)
    else:
        productos_data = db.get_conditional_products()
    categorias = db.get_categories()
    
    return render_template('productos.html', productos=productos_data,categorias=categorias)


@app.route('/admin')
def admin():
    productos_data = db.get_conditional_products()
    categorias = db.get_categories()
    tipos = db.get_types()
    return render_template('Management.html', productos=productos_data,categorias=categorias, tipos=tipos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            precio = request.form.get('precio')
            categoria = request.form.get('categoria')
            tipo = request.form.get('tipo')
            estado = request.form.get('estado')
            descuento = request.form.get('descuento')
            imagen = request.files.get('Imagen')

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
                query = """
                INSERT INTO Productos (
                    Nombre_Producto,
                    Descripcion,
                    Precio,
                    Id_Categoria,
                    Id_Tipo,
                    Estado,
                    Descuento,
                    Imagen
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                );
                """
                conexion.cursor().execute(query, (nombre, descripcion, precio, categoria, tipo, estado, descuento, imagen_url))
                conexion.commit()
                db.products_data = db.get_products_from_db()
                flash('Producto agregado exitosamente', 'success')
            except Exception as e:
                if os.path.exists(imagen_path):
                    os.remove(imagen_path)
                flash(f'Error al agregar producto: {str(e)}', 'error')
            finally:
                conexion.close()

    except Exception as e:
        flash(f'Error al agregar producto: {str(e)}', 'error')
    return redirect(url_for('admin'))

@app.route('/detalles/<int:id>')
def detalles(id):
    producto = db.get_conditional_products(id=id)[0]
    print(producto)
    relacionados = db.get_conditional_products(category=producto.categoria, limit=3, exclude=id)
    return render_template('detalles.html', producto = producto, relacionados = relacionados)


if __name__ == "__main__":
    app.run(debug=True)