from __future__ import unicode_literals

from logging import StreamHandler
import re

from flask import (Flask, jsonify, make_response, redirect, render_template,
                   request, url_for)
from flask.ext.restless import APIManager, simple_serialize
from flask.ext.assets import Environment, Bundle

from models import App, db


web = Flask(__name__)
web.config.from_pyfile('config.py')

assets = Environment(web)
assets.register('js', Bundle('js/*.coffee', filters=['coffeescript', 'jsmin'], output='js/min/show_apps.js'))
assets.register('css', Bundle('css/*.css', filters='cssmin', output='css/min/style.css'))

handler = StreamHandler()
handler.setLevel = web.config.get('LOG_LEVEL', 0)
web.logger.addHandler(handler)

db.init_app(web)
with web.app_context():
    db.create_all()

manager = APIManager(web, flask_sqlalchemy_db=db)
manager.create_api(App, collection_name='apps', methods=['GET', 'DELETE'])
ios_devices_user_agent_re = re.compile(r'iPhone|iPad|iPod')


@web.route('/')
def index():
    return redirect(url_for('show_apps'))


@web.route('/apps/')
def show_apps():
    return render_template('show_apps.html')


@web.route('/apps/<int:id>/manifest.plist')
def manifest_app(id):
    app = App.query.get_or_404(id)
    user_agent = request.headers.get('User-Agent')
    if ios_devices_user_agent_re.search(user_agent):
        app.download_count += 1
        db.session.commit()
    template = render_template('manifest_app.plist', app=app)
    res = make_response(template)
    res.mimetype = 'application/x-apple-plist'
    return res


@web.route('/api/apps', methods=['POST'])
def api_new_app():
    try:
        file = request.files['file']
        app = App.from_file(file)
    except Exception as e:
        web.logger.error('%s', e.message)
        res = jsonify({'message': e.message})
        res.status_code = 400
        return res
    else:
        db.session.add(app)
        db.session.commit()
        return jsonify(simple_serialize(app))


if __name__ == '__main__':
    web.run()
