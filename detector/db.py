import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import flask_sqlalchemy

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


db = flask_sqlalchemy.SQLAlchemy()


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.BLOB, nullable=False)
    label = db.Column(db.String(80), nullable=False)
    objects = db.relationship("Object", back_populates="image")
    
    def __repr__(self):
        return '<Image %r>' % self.label

class Object(db.Model):
    __tablename__ = 'objects'
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)
    name = db.Column(db.String(80), primary_key=True)
    image = db.relationship("Image", back_populates="objects")

    def __repr__(self):
        return '<Object %r>' % self.name
