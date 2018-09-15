# This file is part of the carrier_send_shipments_seurvalencia module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import logging
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Not, Equal
from seurvalencia.picking import *

__all__ = ['CarrierApi']


class CarrierApi(metaclass=PoolMeta):
    __name__ = 'carrier.api'

    @classmethod
    def get_carrier_app(cls):
        'Add Carrier Seur APP'
        res = super(CarrierApi, cls).get_carrier_app()
        res.append(('seurvalencia', 'Seur Valencia'))
        return res

    @classmethod
    def view_attributes(cls):
        return super(CarrierApi, cls).view_attributes() + [
            ('//page[@id="seurvalencia"]', 'states', {
                    'invisible': Not(Equal(Eval('method'), 'seurvalencia')),
                    })]

    @classmethod
    def test_seurvalencia(cls, api):
        'Test Seur Valencia connection'
        message = 'Connection unknown result'

        with API(api.username, api.password, api.debug) as seurvalencia_api:
            message = seurvalencia_api.test_connection()
        cls.raise_user_error(message)
