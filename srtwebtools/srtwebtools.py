from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for, abort, send_file, jsonify, Response, make_response
import pathlib
from os import path
from werkzeug.utils import secure_filename
from functools import wraps
import argparse

from common.utils import projectroot
from common.eventtype import EventType
from translatesrt.translatesrt import TranslateSrt
from translatesrt.translatesrt import Language

from zc.lockfile import LockError

class SrtWebTools:

    app = Flask(__name__)
    ALLOWED_EXTENSIONS = {'srt'}
    current_translation_status = { 'status' : 'idle', 'progress' : 0.0 }

    def __init__(self):
        uploaddir = path.join(projectroot(), 'upload')
        pathlib.Path(uploaddir).mkdir(parents=True, exist_ok=True)
        SrtWebTools.app.secret_key = 'super secret key'
        SrtWebTools.app.config['SESSION_TYPE'] = 'filesystem'
        SrtWebTools.app.config['UPLOAD_FOLDER'] = uploaddir

    def run(self, host):
        SrtWebTools.app.run(host=host)

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
        full_filename = path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], sf)
        translator.subscribe(lambda e: SrtWebTools.handleprogressevent(e))
        try:
            translator.run(full_filename)
        except LockError as e:
            response = jsonify(SrtWebTools.current_translation_status)
            response.status_code = 400
            return response

        file_content = ''
        with open(translator.outputfilename(full_filename)) as f:
            file_content = f.read()

        return jsonify({
                'filename' : secure_filename(translator.outputfilename(secure_filename(filename))),
                'content'  : file_content
            })

    @staticmethod
    def handleprogressevent(e):
        # Don't overwrite value by potential second progress
        if(e.type != EventType.PROGRESS or e.percent == 0):
            return
        SrtWebTools.current_translation_status['status'] = 'busy'
        SrtWebTools.current_translation_status['progress'] = e.percent

    @app.route('/downloadtranslation/<filename>')
    def downloadlocation(filename):
        outputfilename = secure_filename(filename)

        translatedfilepath = path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], outputfilename)
        if path.isfile(translatedfilepath):
            return send_file(translatedfilepath, as_attachment=True)
        else:
            abort(404)

    @app.route('/translation_status')
    def translation_status():
        return jsonify(SrtWebTools.current_translation_status)

    @app.route('/')
    def home():
        return render_template('index.html')


    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in SrtWebTools.ALLOWED_EXTENSIONS



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?', help='listen to address',
            type=str, default='127.0.0.1')
    args = parser.parse_args()
    SrtWebTools().run(args.host)
