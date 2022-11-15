from flask import current_app, g
import click
import psycopg2 as pg2


def get_db():
    if 'db' not in g:
        g.db = pg2.connect(
            dbname=current_app.config['DATABASE'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            host=current_app.config['DATABASE_HOST']
        )

    return g.db


def init_db():
    db = get_db()
    cursor = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))
        cursor.close()
        db.commit()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
