# This file is part of the carrier_send_shipments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from seurvalencia.picking import Picking
from trytond.modules.carrier_send_shipments.tools import unaccent, unspaces
import logging
import tempfile

__all__ = ['ShipmentOut']
__metaclass__ = PoolMeta


class ShipmentOut:
    __name__ = 'stock.shipment.out'

    @classmethod
    def send_seurvalencia(self, api, shipments):
        '''
        Send shipments out to seurvalencia
        :param api: obj
        :param shipments: list
        :param service: obj
        '''
        pool = Pool()
        CarrierApi = pool.get('carrier.api')
        ShipmentOut = pool.get('stock.shipment.out')

        references = []
        labels = []
        errors = []

        default_service = CarrierApi.get_default_carrier_service(api)
        dbname = Transaction().cursor.dbname

        with Picking(api.username, api.password, api.debug) as picking_api:
            for shipment in shipments:
                service = shipment.carrier_service or default_service

                notes = ''
                if shipment.carrier_notes:
                    notes = shipment.carrier_notes

                packages = shipment.number_packages
                if packages == 0:
                    packages = 1

                delivery_name = unaccent(shipment.customer.name)
                if shipment.delivery_address.name:
                    delivery_name = unaccent(shipment.delivery_address.name) 

                data = {}
                #~ data['adn_aduana_destino'] = ''
                #~ data['adn_aduana_origen'] = ''
                #~ data['adn_tipo_mercancia'] = ''
                #~ data['adn_valor_declarado'] = ''
                #~ data['b2c_canal_preaviso1'] = ''
                #~ data['b2c_canal_preaviso2'] = ''
                #~ data['b2c_canal_preaviso3'] = ''
                #~ data['b2c_canal1'] = ''
                #~ data['b2c_canal2'] = ''
                #~ data['b2c_canal3'] = ''
                #~ data['b2c_fecha_entrega'] = ''
                #~ data['b2c_test_llegada'] = ''
                #~ data['b2c_test_preaviso'] = ''
                #~ data['b2c_test_reparto'] = ''
                #~ data['b2c_turno_reparto'] = ''
                data['blt_observaciones'] = unaccent(notes)
                data['blt_referencia'] = shipment.code
                #~ data['cab_producto'] = ''
                #~ data['cab_servicio'] = ''
                data['csg_atencion_de'] = delivery_name
                #~ data['csg_ccc'] = ''
                data['csg_codigo_postal'] = shipment.delivery_address.zip
                #~ data['csg_escalera'] = ''
                data['csg_nombre'] = unaccent(shipment.customer.name)
                data['csg_nombre_via'] = unaccent(shipment.delivery_address.street)
                #~ data['csg_numero_via'] = ''
                data['csg_pais'] = shipment.delivery_address.country.code
                #~ data['csg_piso'] = ''
                data['csg_poblacion'] = unaccent(shipment.delivery_address.city)
                #~ data['csg_puerta'] = ''
                data['csg_telefono'] = unspaces(ShipmentOut.get_phone_shipment_out(shipment))
                #~ data['csg_tipo_numero_via'] = ''
                #~ data['csg_tipo_via'] = ''
                data['exp_bultos'] = packages
                #~ data['exp_cambio'] = ''
                #~ data['exp_cde'] = ''
                data['exp_portes'] = 'F' # F: Facturacion
                if shipment.carrier_cashondelivery:
                    price_ondelivery = ShipmentOut.get_price_ondelivery_shipment_out(shipment)
                    if not price_ondelivery:
                        message = 'Shipment %s not have price and send ' \
                                'cashondelivery' % (shipment.code)
                        errors.append(message)
                        continue
                    data['exp_reembolso'] = 'F' # F: Facturacion
                    data['exp_valor_reembolso'] = str(price_ondelivery)
                else:
                    data['exp_reembolso'] = ' '
                    data['exp_valor_reembolso'] = '0'
                #~ data['exp_seguro'] = ''
                #~ data['exp_entregar_sabado'] = ''
                #~ data['exp_lc'] = ''
                #~ data['exp_observaciones'] = ''
                if api.weight and getattr(shipment, 'weight_func'):
                    data['exp_peso'] = str(shipment.weight_func)
                data['exp_referencia'] = shipment.code
                #~ data['exp_valor_seguro'] = ''
                #~ data['fr_centro_logistico'] = ''
                #~ data['fr_almacenar_hasta'] = ''
                #~ data['fr_tipo_embalaje'] = ''
                #~ data['fr_almacenar_hasta'] = ''
                #~ data['fr_entrega_sabado'] = ''
                #~ data['fr_embalaje'] = ''
                #~ data['fr_etiqueta_control'] = ''
                #~ data['gs_codigo'] = ''
                #~ data['gs_codigo_centro'] = ''
                #~ data['gs_codigo_departamento'] = ''
                #~ data['gs_consolidar_pedido'] = ''
                #~ data['gs_fecha_entrega'] = ''
                #~ data['gs_hora_desde'] = ''
                #~ data['gs_hora_hasta'] = ''
                #~ data['gs_numero_pedido'] = ''
                #~ data['gs_consignatario'] = ''
                #~ data['gs_tipo_mercancia'] = ''
                #~ data['int_divisa'] = ''
                #~ data['int_famimila_mercancia'] = ''
                #~ data['int_producto_mercancia'] = ''
                #~ data['int_codigo_pais'] = ''
                #~ data['int_codigo_postal'] = ''
                #~ data['int_contracto'] = ''
                #~ data['int_extension_direccion'] = ''
                #~ data['int_telefono'] = ''
                #~ data['int_courier'] = ''
                #~ data['int_mercancia'] = ''
                #~ data['int_codigo_pais'] = ''
                #~ data['int_codigo_postal'] = ''
                #~ data['int_valor_declarado'] = ''

                # Send picking data to carrier
                reference, label, error = picking_api.create(data)

                if not reference:
                    logging.getLogger('seurvalencia').error(
                        'Not send shipment %s.' % (shipment.code))
                if reference:
                    self.write([shipment], {
                        'carrier_tracking_ref': reference,
                        'carrier_service': service,
                        'carrier_delivery': True,
                        })
                    logging.getLogger('seurvalencia').info(
                        'Send shipment %s' % (shipment.code))
                    references.append(shipment.code)

                if label:
                    with tempfile.NamedTemporaryFile(
                            prefix='%s-seur-%s-' % (dbname, reference),
                            suffix='.txt', delete=False) as temp:
                        temp.write(label)
                    logging.getLogger('seur').info(
                        'Generated tmp label %s' % (temp.name))
                    temp.close()
                    labels.append(temp.name)
                else:
                    message = 'Not label %s shipment available from Seur.' % (shipment.code)
                    errors.append(message)
                    logging.getLogger('seurvalencia').error(message)

                if error:
                    logging.getLogger('seurvalencia').error(
                        'Not send shipment %s. %s' % (shipment.code, error))
                    errors.append(shipment.code)

        return references, labels, errors

    @classmethod
    def print_labels_seurvalencia(cls, api, shipments):
        '''
        Get labels from shipments out from Seur
        Not available labels from Seur API. Not return labels
        '''
        labels = []
        return labels
