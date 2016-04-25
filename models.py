import os
from uuid import uuid4 as uuid

from flask.ext.sqlalchemy import SQLAlchemy
from ipa import IPAFile
from sqlalchemy import event, sql


db = SQLAlchemy()


class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bundle_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=sql.func.now())
    download_count = db.Column(db.Integer, nullable=False, default=0)
    filename = db.Column(db.String, nullable=False)
    name = db.Column(db.Unicode, nullable=False)
    version = db.Column(db.String, nullable=False)

    @classmethod
    def from_file(cls, file):
        ipa = IPAFile(file)
        _, ext = os.path.splitext(file.filename)
        filename = uuid().hex + ext
        app = cls(bundle_id=ipa.app_info.get('CFBundleIdentifier', ''),
                  filename=filename,
                  name=ipa.get_app_name().decode('utf-8'),
                  version=ipa.get_app_version())
        file.save(os.path.join(db.get_app().config['UPLOAD_DIR'], filename))
        return app

    def _remove_file(self):
        try:
            os.unlink(os.path.join(db.get_app().config['UPLOAD_DIR'], self.filename))
        except (IOError, OSError) as e:
            db.get_app().logger.error('%s', e.message)


@event.listens_for(App, 'after_delete')
def receive_after_delete(mapper, connection, target):
    target._remove_file()
