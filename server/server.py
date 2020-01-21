"""Запуск сайта с возможностью загрузки"""

__author__ = 'alexander'
__maintainer__ = 'alexander'
__credits__ = ['alexander', ]
__copyright__ = "LGPL"
__status__ = 'Development'
__version__ = '20200121'


from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from workers.solver import *
import redis
import hashlib
import os

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = ['png']

app = Flask(__name__, template_folder="../server/")
app.config['MAX_CONTENT_LENGTH'] = 32*1024*1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def _allowed_file(filename):
    """Проверка загружаемого файла (доступ только для png)"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['post', 'get'])
def _index():
    """Главная страница с загрузкой файла"""
    if request.method == 'POST':
        file = request.files['file']
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = open('{}/{}'.format(UPLOAD_FOLDER, filename), 'rb')
            data = file.read()
            fn = int(hashlib.sha1(data).hexdigest(), 16)
            file.close()
            produce(UPLOAD_FOLDER, filename, fn)
            return redirect(url_for('_uploaded_file', filename=fn))

    return render_template('templates/index.html')


@app.route('/result/<filename>')
def _uploaded_file(filename):
    """Страница с результатом для отправленного файла"""
    r = redis.StrictRedis()
    message = 'Пожалуйста подождите'
    try:
        message = r.get(filename).decode('utf-8')
    except AttributeError:
        pass
    return render_template('templates/result.html', message=message)

