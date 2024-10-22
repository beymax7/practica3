from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesaria para usar session

# Inicializamos una lista vacía en la sesión
@app.before_request
def initialize_session():
    if 'inscritos' not in session:
        session['inscritos'] = []

@app.route('/')
def lista_inscritos():
    return render_template('index.html', inscritos=session['inscritos'])

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        inscrito = {
            'id': len(session['inscritos']) + 1,
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': '; '.join(seminarios)
        }

        session['inscritos'].append(inscrito)
        session.modified = True
        return redirect(url_for('lista_inscritos'))
    return render_template('form.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    inscritos = session['inscritos']
    inscrito = next((i for i in inscritos if i['id'] == id), None)
    
    if request.method == 'POST':
        inscrito['fecha'] = request.form['fecha']
        inscrito['nombre'] = request.form['nombre']
        inscrito['apellidos'] = request.form['apellidos']
        inscrito['turno'] = request.form['turno']
        inscrito['seminarios'] = '; '.join(request.form.getlist('seminarios'))
        session.modified = True
        return redirect(url_for('lista_inscritos'))
    
    return render_template('form.html', inscrito=inscrito)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    # Eliminar el inscrito
    session['inscritos'] = [i for i in session['inscritos'] if i['id'] != id]
    
    # Re-asignar los IDs para que sean consecutivos
    for idx, inscrito in enumerate(session['inscritos']):
        inscrito['id'] = idx + 1  # Los IDs empiezan desde 1

    # Guardar la sesión modificada
    session.modified = True
    return redirect(url_for('lista_inscritos'))


if __name__ == '__main__':
    app.run(debug=True)
