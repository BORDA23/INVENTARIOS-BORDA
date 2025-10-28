from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Función para obtener conexión a la base de datos
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar base de datos
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            estado TEXT NOT NULL,
            ubicacion TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_equipo INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion TEXT,
            FOREIGN KEY (id_equipo) REFERENCES equipos (id),
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/equipos')
def equipos():
    conn = get_db()
    equipos = conn.execute('SELECT * FROM equipos').fetchall()
    conn.close()
    return render_template('equipos/index.html', equipos=equipos)

@app.route('/equipos/crear', methods=['GET', 'POST'])
def crear_equipo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        estado = request.form['estado']
        ubicacion = request.form['ubicacion']
        
        conn = get_db()
        conn.execute('INSERT INTO equipos (nombre, estado, ubicacion) VALUES (?, ?, ?)',
                     (nombre, estado, ubicacion))
        conn.commit()
        conn.close()
        
        flash('Equipo creado exitosamente', 'success')
        return redirect(url_for('equipos'))
    
    return render_template('equipos/crear.html')

@app.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    conn = get_db()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        estado = request.form['estado']
        ubicacion = request.form['ubicacion']
        
        conn.execute('UPDATE equipos SET nombre=?, estado=?, ubicacion=? WHERE id=?',
                     (nombre, estado, ubicacion, id))
        conn.commit()
        conn.close()
        
        flash('Equipo actualizado exitosamente', 'success')
        return redirect(url_for('equipos'))
    
    equipo = conn.execute('SELECT * FROM equipos WHERE id=?', (id,)).fetchone()
    conn.close()
    
    return render_template('equipos/editar.html', equipo=equipo)

@app.route('/equipos/eliminar/<int:id>')
def eliminar_equipo(id):
    conn = get_db()
    conn.execute('DELETE FROM equipos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    
    flash('Equipo eliminado exitosamente', 'success')
    return redirect(url_for('equipos'))

@app.route('/usuarios')
def usuarios():
    conn = get_db()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('usuarios/index.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cargo = request.form['cargo']
        
        conn = get_db()
        conn.execute('INSERT INTO usuarios (nombre, cargo) VALUES (?, ?)',
                     (nombre, cargo))
        conn.commit()
        conn.close()
        
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('usuarios'))
    
    return render_template('usuarios/crear.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        cargo = request.form['cargo']
        
        conn.execute('UPDATE usuarios SET nombre=?, cargo=? WHERE id=?',
                     (nombre, cargo, id))
        conn.commit()
        conn.close()
        
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('usuarios'))
    
    usuario = conn.execute('SELECT * FROM usuarios WHERE id=?', (id,)).fetchone()
    conn.close()
    
    return render_template('usuarios/editar.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    conn = get_db()
    conn.execute('DELETE FROM usuarios WHERE id=?', (id,))
    conn.commit()
    conn.close()
    
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('usuarios'))

@app.route('/prestamos')
def prestamos():
    conn = get_db()
    prestamos = conn.execute('''
        SELECT p.*, e.nombre as equipo_nombre, u.nombre as usuario_nombre
        FROM prestamos p
        JOIN equipos e ON p.id_equipo = e.id
        JOIN usuarios u ON p.id_usuario = u.id
        ORDER BY p.fecha_prestamo DESC
    ''').fetchall()
    conn.close()
    return render_template('prestamos/index.html', prestamos=prestamos)

@app.route('/prestamos/crear', methods=['GET', 'POST'])
def crear_prestamo():
    conn = get_db()
    
    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        id_usuario = request.form['id_usuario']
        fecha_prestamo = request.form['fecha_prestamo']
        
        conn.execute('INSERT INTO prestamos (id_equipo, id_usuario, fecha_prestamo) VALUES (?, ?, ?)',
                     (id_equipo, id_usuario, fecha_prestamo))
        conn.commit()
        conn.close()
        
        flash('Préstamo registrado exitosamente', 'success')
        return redirect(url_for('prestamos'))
    
    equipos = conn.execute('SELECT * FROM equipos').fetchall()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    
    return render_template('prestamos/crear.html', equipos=equipos, usuarios=usuarios)

@app.route('/prestamos/editar/<int:id>', methods=['GET', 'POST'])
def editar_prestamo(id):
    conn = get_db()
    
    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        id_usuario = request.form['id_usuario']
        fecha_prestamo = request.form['fecha_prestamo']
        fecha_devolucion = request.form['fecha_devolucion']
        
        conn.execute('''UPDATE prestamos SET id_equipo=?, id_usuario=?, 
                        fecha_prestamo=?, fecha_devolucion=? WHERE id=?''',
                     (id_equipo, id_usuario, fecha_prestamo, fecha_devolucion, id))
        conn.commit()
        conn.close()
        
        flash('Préstamo actualizado exitosamente', 'success')
        return redirect(url_for('prestamos'))
    
    prestamo = conn.execute('SELECT * FROM prestamos WHERE id=?', (id,)).fetchone()
    equipos = conn.execute('SELECT * FROM equipos').fetchall()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    
    return render_template('prestamos/editar.html', prestamo=prestamo, equipos=equipos, usuarios=usuarios)

@app.route('/prestamos/eliminar/<int:id>')
def eliminar_prestamo(id):
    conn = get_db()
    conn.execute('DELETE FROM prestamos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    
    flash('Préstamo eliminado exitosamente', 'success')
    return redirect(url_for('prestamos'))

@app.route('/prestamos/devolver/<int:id>')
def devolver_prestamo(id):
    conn = get_db()
    fecha_devolucion = datetime.now().strftime('%Y-%m-%d')
    conn.execute('UPDATE prestamos SET fecha_devolucion=? WHERE id=?', (fecha_devolucion, id))
    conn.commit()
    conn.close()
    
    flash('Devolución registrada exitosamente', 'success')
    return redirect(url_for('prestamos'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)