from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Configuración de la base de datos (se crea un archivo biblioteca.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS (TABLAS DE LA BASE DE DATOS) ---
class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Integer, default=1)
    prestados = db.Column(db.Integer, default=0)

class Prestamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libro.id'))
    alumno_nombre = db.Column(db.String(100), nullable=False)
    alumno_email = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    libro = db.relationship('Libro', backref='lista_prestamos')

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# --- RUTAS (LO QUE VES EN EL NAVEGADOR) ---
@app.route('/')
def index():
    libros = Libro.query.all()
    prestamos = Prestamo.query.all()
    return render_template('index.html', libros=libros, prestamos=prestamos)

@app.route('/nuevo_libro', methods=['POST'])
def nuevo_libro():
    titulo = request.form.get('titulo')
    cantidad = int(request.form.get('cantidad'))
    nuevo = Libro(titulo=titulo, total=cantidad)
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/prestar', methods=['POST'])
def prestar():
    libro_id = request.form.get('libro_id')
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    
    libro = Libro.query.get(libro_id)
    if libro and libro.prestados < libro.total:
        libro.prestados += 1
        nuevo_prestamo = Prestamo(libro_id=libro.id, alumno_nombre=nombre, alumno_email=email)
        db.session.add(nuevo_prestamo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/devolver/<int:id>')
def devolver(id):
    prestamo = Prestamo.query.get(id)
    if prestamo:
        libro = Libro.query.get(prestamo.libro_id)
        libro.prestados -= 1
        db.session.delete(prestamo)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # IMPORTANTE: host='0.0.0.0' permite que Docker vea la app
    app.run(debug=True, host='0.0.0.0', port=5000)