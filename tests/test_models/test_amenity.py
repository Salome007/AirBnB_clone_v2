#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
import unittest
from models.amenity import Amenity


@unittest.skip("skip for DB storage")
class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
