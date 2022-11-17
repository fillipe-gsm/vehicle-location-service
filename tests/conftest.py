import peewee as pw
import pytest

from vehicle_location_service.models import Vehicle


MODELS = [Vehicle]

test_db = pw.SqliteDatabase(":memory:")


@pytest.fixture
def test_database():
    test_db.bind(MODELS)
    test_db.connect()
    test_db.create_tables(MODELS)

    yield test_db

    test_db.drop_tables(MODELS)
    test_db.close()
