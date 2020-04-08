from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for, abort, send_file
import pathlib
from os import path
from werkzeug.utils import secure_filename

from common.utils import projectroot
from translatesrt.translatesrt import TranslateSrt
from translatesrt.translatesrt import Language


class SrtWebTools:

    app = Flask(__name__)
    ALLOWED_EXTENSIONS = {'srt'}

    def __init__(self):
        uploaddir = path.join(projectroot(), 'upload')
        pathlib.Path(uploaddir).mkdir(parents=True, exist_ok=True)
        SrtWebTools.app.secret_key = 'super secret key'
        SrtWebTools.app.config['SESSION_TYPE'] = 'filesystem'
        SrtWebTools.app.config['UPLOAD_FOLDER'] = uploaddir

    def run(self):
        SrtWebTools.app.run()

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(SrtWebTools.app.config['UPLOAD_FOLDER'],filename)

    @app.route('/upload', methods = ['POST'])
    def upload():
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        if file and SrtWebTools.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], filename))
        return redirect('/?filename=' + file.filename)

    @app.route('/translate/<filename>', methods={'POST'})
    def translate(filename):
        sf = secure_filename(filename)
        translator = TranslateSrt(Language.FR, Language.EN)
        translator.run(path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], sf))
        return send_from_directory(SrtWebTools.app.config['UPLOAD_FOLDER'], translator.outputfilename(sf))

    @app.route('/downloadtranslation/<filename>')
    def downloadlocation(filename):
        translator = TranslateSrt(Language.FR, Language.EN);
        outputfilename = secure_filename(translator.outputfilename(secure_filename(filename)))
        translatedfilepath = path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], outputfilename)
        if path.isfile(translatedfilepath):
            return send_file(translatedfilepath, as_attachment=True)  # SrtWebTools.UPLOAD_PATH + '/' + outputfilename
        else:
            abort(404)

    @app.route('/')
    def home():
        return render_template('index.html')


    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in SrtWebTools.ALLOWED_EXTENSIONS

def main():
    SrtWebTools().run()
