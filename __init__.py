# This file is part of carrier_send_shipments_seurvalencia module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# copyright notices and license terms. the full
from trytond.pool import Pool
from .api import *
from .shipment import *
from .manifest import *


def register():
    Pool.register(
        CarrierApi,
        ShipmentOut,
        module='carrier_send_shipments_seurvalencia', type_='model')
    Pool.register(
        CarrierManifest,
        module='carrier_send_shipments_seurvalencia', type_='wizard')
