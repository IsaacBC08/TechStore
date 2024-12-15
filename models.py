class Producto:
    def __init__(self,id, nombre, imagen, precio, descripcion,categoria, estado, descuento, tipo):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria
        self.tipo = tipo
        self.estado = estado
        self.descuento = descuento if descuento else 0
        self.imagen = imagen

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "descuento": self.descuento,
        }
    @classmethod
    def crear_desde_registro(cls, fila):
        """Crea un objeto Producto desde un registro de la base de datos."""
        return cls(
            id=fila['Id_Producto'],
            nombre=fila['Nombre_Producto'],
            precio=fila['Precio'],
            descripcion=fila['Descripcion'],
            categoria=fila['Categoría'],
            estado=fila['Estado'],
            descuento= fila['Descuento'],
            imagen=fila['Imagen'],
            tipo=fila['Tipo']
        )

class Categoria:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
    
    @classmethod
    def crear_desde_registro(cls, fila):
        """Crea un objeto Categoría desde un registro de la base de datos."""
        return cls(
            id= fila['Id_Categoria'],
            nombre = fila['Nombre_Categoria']
            
        )

class Tipo:
    def __init__(self, id, nombre,categoria_id, categoria):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.categoria_id = categoria_id
    
    @classmethod
    def crear_desde_registro(cls, fila):
        """Crea un objeto Categoría desde un registro de la base de datos."""
        return cls(
            id= fila['Id_Categoria'],
            nombre = fila['Nombre_Tipo'],
            categoria_id = fila['Id_Categoria'],
            categoria= fila['categoria']
        )