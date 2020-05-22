import os
import tempfile

from influxdb import InfluxDBClient

import pytest as py

from data_pipeline.daten_filtern.src.filtern_api import filtern_api


@py.fixture
def client():
    db_fd, filtern_api.app.config['DATABASE'] = tempfile.mkstemp()
    filtern_api.app.config['TESTING'] = True

    with filtern_api.app.test_client() as client:
        with filtern_api.app.app_context():
            filtern_api.init_db()
        yield client

    os.close(db_fd)
    os.unlink(filtern_api.app.config['DATABASE'])