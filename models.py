class Producto:
    def __init__(self,id, nombre, imagen, precio, descripcion):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.imagen = imagen

    @classmethod
    def crear_desde_registro(cls, fila):
        """Crea un objeto Producto desde un registro de la base de datos."""
        return cls(
            id=fila['Id_Producto'],
            nombre=fila['Nombre_Producto'],
            precio=fila['Precio'],
            descripcion=fila['Descripcion'],
            imagen=fila['Imagen']
        )
