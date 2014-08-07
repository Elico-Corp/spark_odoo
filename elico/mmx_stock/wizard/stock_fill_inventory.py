# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#     Jon Chow <jon.chow@elico-corp.com>
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

from openerp.osv import osv


class stock_fill_inventory(osv.osv_memory):
    _inherit = "stock.fill.inventory"

    def _get_default_location(self, cr, uid, context=None):
        company_id = self.pool.get('res.company')._company_default_get(
            cr, uid, 'stock.inventory', context=context),
        location_pool = self.pool.get('stock.location')
        ids = location_pool.search(
            cr, uid, [('company_id', '=', company_id),
                      ('usage', '=', 'internal'),
                      ('name', 'ilike', 'stock')])
        return ids and ids[0] or False

    _defaults = {
        'location_id': lambda self, cr, uid, c: self._get_default_location(
            cr, uid, context=c)
    }

    def fill_inventory_by_all_product(self, cr, uid, ids, context=None):
        """
        fill inventory by all product
        """
        inventory_line_obj = self.pool.get('stock.inventory.line')

        wiz = self.browse(cr, uid, ids[0], context=None)
        inventory_id = context.get('active_id', False)
        location_id = wiz.location_id.id
        inventory = self.pool.get('stock.inventory').browse(cr, uid,
                                                            inventory_id)
        company_id = inventory.company_id.id

        cr.execute(
            '''
            select pp.id, pt.uom_id
            from product_product as pp
                left join product_template as pt on
                                    (pp.product_tmpl_id = pt.id);
            '''
        )
        pdt_umo_ids = cr.fetchall()

        for pdt_umo in pdt_umo_ids:
            inventory_line_obj.create(cr, uid, {
                'inventory_id': inventory_id,
                'location_id': location_id,
                'product_id': pdt_umo[0],
                'product_qty': 0,
                'product_uom': pdt_umo[1],
                'company_id': company_id,
            })
        return {'type': 'ir.actions.act_window_close'}
stock_fill_inventory()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
