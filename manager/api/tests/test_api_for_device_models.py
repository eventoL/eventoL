import unittest
from manager.models import HardwareManufacturer, Software, Hardware
from manager.api.tests.test_api import api_test


# Device Models
@api_test()
class TestApiHardwareManufacturer():
    str_model = 'manager.HardwareManufacturer'
    model = HardwareManufacturer
    url_base = '/api/hardwaremanufacturer/'
    example = {
        'name': 'Manufacturer'
    }


@api_test()
class TestApiSoftware():
    str_model = 'manager.Software'
    model = Software
    url_base = '/api/software/'
    example = {
        'name': 'eventoL',
        'version': 'v2.0'
    }
    # TODO View 'type': 'Other'


@api_test()
class TestApiHardware():
    fk_models = ['manager.HardwareManufacturer']
    str_model = 'manager.Hardware'
    model = Hardware
    url_base = '/api/hardware/'
    example = {
        'model': 'model',
        'serial': '19827398172ASDF'
    }
    # TODO View 'type': 'Other'

if __name__ == '__main__':
    unittest.main()

