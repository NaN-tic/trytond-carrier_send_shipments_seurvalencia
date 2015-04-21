# This file is part of carrier_send_shipments_seurvalencia module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from seurvalencia import Picking
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from base64 import decodestring

__all__ = ['CarrierManifest']
__metaclass__ = PoolMeta


class CarrierManifest:
    __name__ = 'carrier.manifest'

    def get_manifest_seurvalencia(self, api, from_date, to_date):
        dbname = Transaction().cursor.dbname

        with Picking(api.username, api.password, api.debug) as picking_api:
            manifest_file = picking_api.info()
            if manifest_file:
                manifiest = decodestring(manifest_file)
                file_name = '%s-manifest-seurvalencia.pdf' % dbname
                return (manifiest, file_name)
            else:
                return
