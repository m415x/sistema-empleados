from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime
import os


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_PORT'] = '3306' # 404
app.config['MYSQL_DATABASE_DB'] = 'empleados'
app.config['UPLOADS'] = os.path.join('uploads') # Guardamos la ruta de fotos como un valor en la app

UPLOADS = app.config['UPLOADS']

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


# * QUERY-MYSQL * ------------------------------------------------------------------------------
# def queryMySQL(query, data=()):
#     if len(data) > 0:
#         cursor.execute(query, data)
#     else:
#         cursor.execute(query)
#     conn.commit()
#     return cursor.


# * USERPIC * ----------------------------------------------------------------------------------
@app.route('/userpic/<path:nombreFoto>')
def uploads(nombreFoto):

    return send_from_directory(os.path.join('uploads'), nombreFoto)


# * INDEX * ------------------------------------------------------------------------------------
@app.route('/')
def index():

    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)
    empleados = cursor.fetchall()
    
    conn.commit()

    return render_template('empleados/index.html', empleados=empleados)


# * CREATE * -----------------------------------------------------------------------------------
@app.route('/create')
def create():

    return render_template('empleados/create.html')


# * STORE * ------------------------------------------------------------------------------------
@app.route('/store', methods=['POST'])
def storage():
    
    sql = "INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s);"
    # f"INSERT INTO empleados (nombre, correo, foto) VALUES ({_nombre}, {_correo}, {nuevoNombreFoto});" y eliminar datos
    
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    now = datetime.now()  # Fecha y hora de subida
    tiempo = now.strftime('%Y%H%M%S')
    nuevoNombreFoto = ''

    if _foto.filename != '':
        nuevoNombreFoto = f"{tiempo}_{_foto.filename}"
        _foto.save('uploads/' + nuevoNombreFoto)

    datos = (_nombre, _correo, nuevoNombreFoto)

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


# * DELETE * -----------------------------------------------------------------------------------
@app.route('/delete/<int:id>')
def delete(id):

    sql = f"SELECT foto FROM empleados WHERE id={id};"
    cursor.execute(sql)

    nombreFoto = cursor.fetchone()[0]

    try:
        os.remove(os.path.join(UPLOADS, nombreFoto))
    except:
        pass

    sql = f"DELETE FROM empleados WHERE id={id};"
    cursor.execute(sql)

    conn.commit()

    return redirect('/')


# * MODIFY * -----------------------------------------------------------------------------------
@app.route('/modify/<int:id>')
def modify(id):

    sql = f"SELECT * FROM empleados WHERE id={id};"
    cursor.execute(sql)
    empleado = cursor.fetchone()  # Trae un solo empleado

    conn.commit()

    return render_template('empleados/edit.html', empleado=empleado)


# * UPDATE * -----------------------------------------------------------------------------------
@app.route('/update', methods=['POST'])
def update():

    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime('%Y%H%M%S')
        nuevoNombreFoto = f"{tiempo}_{_foto.filename}"
        _foto.save('uploads/' + nuevoNombreFoto)

        sql = f"SELECT foto FROM empleados WHERE id={id};"
        cursor.execute(sql)
        conn.commit()

        nombreFoto = cursor.fetchone()[0]

        try:
            os.remove(os.path.join(UPLOADS, nombreFoto))
        except:
            pass

        sql = f"UPDATE empleados SET foto='{nuevoNombreFoto}' WHERE id={id};"
        cursor.execute(sql)
        conn.commit()

    sql = f"UPDATE empleados SET nombre='{_nombre}', correo='{_correo}' WHERE id={id};"
    cursor.execute(sql)
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
