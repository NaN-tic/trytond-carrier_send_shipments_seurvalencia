# This file is part of the carrier_send_shipments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

import logging

try:
    from seurvalencia.picking import *
except ImportError:
    message = 'Install Seur from Pypi: pip install seurvalencia'
    logging.getLogger('seurvalencia').error(message)
    raise Exception(message)

__all__ = ['CarrierApi']
__metaclass__ = PoolMeta


class CarrierApi:
    __name__ = 'carrier.api'

    @classmethod
    def get_carrier_app(cls):
        '''
        Add Carrier Seur APP
        '''
        res = super(CarrierApi, cls).get_carrier_app()
        res.append(('seurvalencia', 'Seur Valencia'))
        return res

    def test_seurvalencia(self, api):
        '''
        Test Seur Valencia connection
        :param api: obj
        '''
        message = 'Connection unknown result'
        
        seurvalencia_context = {}
        with API(api.username, api.password, api.debug) as seurvalencia_api:
            message = seurvalencia_api.test_connection()
        self.raise_user_error(message)
