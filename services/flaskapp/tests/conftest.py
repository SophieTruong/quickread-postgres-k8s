"""
This file describes fixtures for setting up
and tearing down testing all functions
"""
# pylint: disable=wrong-import-position,unused-argument,redefined-outer-name
import sys
# sys.path.append('../')

from os.path import abspath, dirname
package_path = abspath(dirname(dirname(__file__)))
sys.path.insert(0, package_path)


import pytest  # noqa: E402

from src import app  # noqa: E402
from src.models import db, UnlabeledData  # noqa: E402


@pytest.fixture(scope='module')
def test_client():
    """
    Create for test_client
    """
    app.testing = True

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def unlabeled_data():
    """
    Create unlabel_data to based on models.py
    """
    new_unlabeled_data = UnlabeledData('Foo bar', 'Foo bar')
    return new_unlabeled_data


@pytest.fixture(scope='module')
def init_database(test_client):
    """
    Initialize the database
    """
    # Create the database and the database table
    db.create_all()

    # Insert user data
    data1 = UnlabeledData('Foo bar', 'Foo bar')
    data2 = UnlabeledData('foobar', 'foobar')
    db.session.add(data1)
    db.session.add(data2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()
