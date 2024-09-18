from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from kerykeion import AstrologicalSubject, RelationshipScore
import os

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración para la carga de archivos
# Se define la carpeta donde se almacenarán las imágenes subidas
UPLOAD_FOLDER = 'imagenes'
# Se definen las extensiones de archivo permitidas para las imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta de uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para verificar si la extensión de un archivo es permitida
def allowed_file(filename):
    # Divide el nombre del archivo por el punto y verifica la extensión
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Definición de la ruta y método para la API
@app.route('/relationship_score', methods=['POST'])
def calculate_relationship_score():
    # Comprobación de que hay archivos en la petición
    # Retorna error si no se encuentran archivos 'file1' y 'file2'
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Comprobación de que los archivos han sido seleccionados y son válidos
    if file1.filename == '' or file2.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        # Asegurar que el nombre del archivo es seguro
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        # Guardar los archivos en la carpeta designada
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

    # Obtener los datos del formulario
    data = request.form
    # Crear objetos AstrologicalSubject para cada persona
    persona1 = AstrologicalSubject(
        "Persona1",
        int(data['persona1[año]']),
        int(data['persona1[mes]']),
        int(data['persona1[dia]']),
        int(data['persona1[hora]']),
        int(data['persona1[minuto]']),
        data['persona1[ciudad]'],
        data['persona1[pais]']
    )

    persona2 = AstrologicalSubject(
        "Persona2",
        int(data['persona2[año]']),
        int(data['persona2[mes]']),
        int(data['persona2[dia]']),
        int(data['persona2[hora]']),
        int(data['persona2[minuto]']),
        data['persona2[ciudad]'],
        data['persona2[pais]']
    )

    # Calcular la puntuación de la relación usando kerykeion
    puntuacion_relacion = RelationshipScore(persona1, persona2)

    # Devolver la puntuación en formato JSON
    return jsonify({"puntuacion": puntuacion_relacion.score})

# Ejecutar la aplicación si este script es el principal
if __name__ == '__main__':
    app.run(debug=True)