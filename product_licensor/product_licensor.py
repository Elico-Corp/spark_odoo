# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2015 Elico Corp (<http://www.elico-corp.com>)
#     <alex.duan@elico-corp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields
from openerp.tools.translate import _


class ProductProduct(orm.Model):
    _inherit = 'product.product'
    _columns = {
        'licensor_ids': fields.many2many(
            'res.partner', 'product_licensor_rel', 'product_id', 'licensor_id',
            'Licensors'),
    }


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'is_licensor': fields.boolean(
            'Is Licensor',
            groups="product_licensor.group_licensor_manager"),
        'number_of_samples': fields.integer(
            'Number of samples to send',
            groups="product_licensor.group_licensor_manager"),
        'contract_number': fields.char(
            'Contract Number', size=125,
            groups="product_licensor.group_licensor_manager"),
        'licensed_product_ids': fields.many2many(
            'product.product', 'product_licensor_rel', 'licensor_id',
            'product_id', 'Licensed Products',
            groups="product_licensor.group_licensor_manager"),
        'field_percentage': fields.integer(
            'Field Percentage (%)',
            groups="product_licensor.group_licensor_manager",
            help=_('Percentage of the sales to pay to licensor'))
    }
    _defaults = {
        'is_licensor': False,
    }
