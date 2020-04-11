from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for, abort, send_file, jsonify, Response, make_response
import pathlib
from os import path
from werkzeug.utils import secure_filename
from functools import wraps
import argparse
import base64
import binascii

from common.utils import projectroot
from common.eventtype import EventType
from translatesrt.translatesrt import TranslateSrt
from translatesrt.translatesrt import Language

from zc.lockfile import LockError
from requests import exceptions

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
        try:
            filename_decoded = str(base64.urlsafe_b64decode(filename.encode('utf-8')), 'utf-8')
        except (UnicodeDecodeError, binascii.Error):
            errorDict = {'error' : UnicodeDecodeError.__name__, 'value' : dict() }
            response = jsonify(errorDict)
            response.status_code = 400
            return response

        sf = secure_filename(filename_decoded)
        full_filename = path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], sf)
        if path.isfile(full_filename):
            return send_from_directory(SrtWebTools.app.config['UPLOAD_FOLDER'], sf)
        else:
            return SrtWebTools.file_not_found(filename_decoded)

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
        return redirect('/?filename=' + str(base64.urlsafe_b64encode(file.filename.encode("utf-8")), 'utf-8'))

    @app.route('/translate/<filename>', methods={'POST'})
    def translate(filename):
        filename_decoded = str(base64.urlsafe_b64decode(filename.encode('utf-8')), 'utf-8')
        sf = secure_filename(filename_decoded)
        translator = TranslateSrt(Language.FR, Language.EN)
        full_filename = path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], sf)
        translator.subscribe(lambda e: SrtWebTools.handleprogressevent(e))
        try:
            translator.run(full_filename)
        except LockError:
            errorDict = {
                        'error' : LockError.__name__,
                        'value' : SrtWebTools.current_translation_status
                        }
            response = jsonify(errorDict)
            response.status_code = 400
            return response
        except exceptions.ConnectionError:
            errorDict = {'error' : exceptions.ConnectionError.__name__, 'value' : dict() }
            response = jsonify(errorDict)
            response.status_code = 500
            return response
        except FileNotFoundError:
            return SrtWebTools.file_not_found(filename_decoded)

        file_content = ''
        with open(translator.outputfilename(full_filename)) as f:
            file_content = f.read()
        secured_output_filename = secure_filename(translator.outputfilename(sf))
        return jsonify({
                'filename' : str(base64.urlsafe_b64encode(secured_output_filename.encode("utf-8")), 'utf-8'),
                'content'  : file_content
            })

    @staticmethod
    def file_not_found(filename):
        errorDict = {'error' : FileNotFoundError.__name__, 'value' : { 'filename' : filename } }
        response = jsonify(errorDict)
        response.status_code = 404
        return response

    @staticmethod
    def handleprogressevent(e):
        # Don't overwrite value by potential second progress
        if(e.type != EventType.PROGRESS or e.percent == 0):
            return
        SrtWebTools.current_translation_status['status'] = 'busy'
        SrtWebTools.current_translation_status['progress'] = e.percent

    @app.route('/downloadtranslation/<filename>')
    def downloadlocation(filename):
        filename_decoded = str(base64.urlsafe_b64decode(filename.encode('utf-8')), 'utf-8')
        outputfilename = secure_filename(filename_decoded)

        translatedfilepath = path.join(SrtWebTools.app.config['UPLOAD_FOLDER'], outputfilename)
        if path.isfile(translatedfilepath):
            return send_file(translatedfilepath, as_attachment=True)
        else:
            return SrtWebTools.file_not_found(filename_decoded)

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
