# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo.tests.common import TransactionCase
from odoo.addons.sale.tests import test_sale_common


class SaleCommon(test_sale_common.TestSale):

    def setUp(self):
        super(SaleCommon, self).setUp()
        for product in self.products.values():
            product.standard_price = 0

    def _create_sale(self):
        sale = self.env['sale.order'].sudo(self.user).create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'order_line': [
                (0, 0, {'name': p.name,
                        'product_id': p.id,
                        'product_uom_qty': 2,
                        'product_uom': p.uom_id.id,
                        'price_unit': p.list_price})
                for (_, p) in self.products.iteritems()
            ],
            'pricelist_id': self.env.ref('product.list0').id,
        })
        return sale


class ProductCommon(TransactionCase):

    def setUp(self):
        super(ProductCommon, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'standard_price': 0,
        })
        self.base_currency = self.env.ref('base.EUR')
        self.company = self.env.ref('base.main_company')
        self.company.currency_id = self.base_currency

    def _create_history_cost(self, product, cost):
        self.env['product.price.history'].create({
            'product_id': product.id,
            'company_id': self.company.id,
            'cost': cost,
        })
