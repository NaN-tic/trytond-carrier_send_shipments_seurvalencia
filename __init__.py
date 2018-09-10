# This file is part of carrier_send_shipments_seurvalencia module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# copyright notices and license terms. the full
from trytond.pool import Pool
from . import api
from . import shipment
from . import manifest


def register():
    Pool.register(
        api.CarrierApi,
        shipment.ShipmentOut,
        module='carrier_send_shipments_seurvalencia', type_='model')
    Pool.register(
        manifest.CarrierManifest,
        module='carrier_send_shipments_seurvalencia', type_='wizard')
