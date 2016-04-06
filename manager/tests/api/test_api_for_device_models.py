import unittest
from manager.models import Software, Hardware
from manager.tests.api.test_api import api_test


# Device Models
@api_test()
class TestApiSoftware():
    str_model = 'manager.Software'
    model = Software
    url_base = '/api/softwares/'
    example = {
        'name': 'eventoL'
    }
    # TODO View 'type': 'Other'


@api_test()
class TestApiHardware():
    fk_models = []
    str_model = 'manager.Hardware'
    model = Hardware
    url_base = '/api/hardwares/'
    example = {
        'model': 'model',
        'manufacturer': '19827398172ASDF'
    }
    # TODO View 'type': 'Other'
