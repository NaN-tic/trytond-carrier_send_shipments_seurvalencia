# This file is part of the carrier_send_shipments_seurvalencia module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class CarrierSendShipmentsSeurvalenciaTestCase(ModuleTestCase):
    'Test Carrier Send Shipments Seurvalencia module'
    module = 'carrier_send_shipments_seurvalencia'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CarrierSendShipmentsSeurvalenciaTestCase))
    return suite