''' Management '''
from flask.cli import FlaskGroup
from src import app
from src.models import db,UnlabeledData

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    """
    Create db and initialize the tables
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    """
    Add seed data to db
    """
    db.session.add(UnlabeledData(raw_text_input="Hi Mom, how are you today?"))
    db.session.commit()

if __name__ == "__main__":
    cli()
