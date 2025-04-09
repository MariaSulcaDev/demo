from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from  flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
CORS(app)#PERMITE PETIVCIONES DESDE REACT

#CONFIGURAR EL QSlALCHEMY CON ORACLE CLOUD
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#CONFIGURAR EL QSlALCHEMY CON ORACLE CLOUD
db = SQLAlchemy(app)

#DEFINIR EL MODELO DE LA BASE DE DATOS
class Producto(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {	
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio
        }
#crear  las tablas en la base de datos
with app.app_context():
    db.create_all()

#RUTA PARA OBTENER TODOS LOS PRODUCTOS
# Definir el modelo de la base de datos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "precio": self.precio}

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# RUTA PARA OBTENER TODOS LOS PRODUCTOS 
@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos])
    
# RUTA PARA  PARA OBTENER UN  PRODUCTO POR ID
@app.route('/productos/<int:id>', methods=['GET'])
def get_producto_por_id(id):
    producto = Producto.query.get(id)
    if producto:
        return jsonify(producto.to_dict()), 200
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404


# RUTA PARA CREAR UN NUEVO PRODUCTO
@app.route('/productos', methods=['POST'])
def create_producto():
    try:
        data = request.get_json()
        if not data or 'nombre' not in data or 'precio' not in data:
            return jsonify({'error': 'Datos incompletoss'}), 400
        
        nuevo_producto = Producto(nombre=data['nombre'], precio=data['precio'])
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify(nuevo_producto.to_dict()), 201
    except Exception as e:
        return jsonify({'error': f'Error al crear producto: {str(e)}'}), 500

# RUTA PARA ACTUALIZAR UN PRODUCTO
@app.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    try:
        data = request.get_json()
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404

        if 'nombre' in data:
            producto.nombre = data['nombre']
        if 'precio' in data:
            producto.precio = data['precio']
        
        db.session.commit()
        return jsonify(producto.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Error al actualizar producto: {str(e)}'}), 500

# RUTA PARA ELIMINAR UN PRODUCTO
@app.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'message': f'Producto con ID {id} eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al eliminar producto: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)


    