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

import time
from openerp.report import report_sxw
from openerp.osv import osv


class sale_order_line(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_order_line, self).__init__(cr, uid, name, context=context)
        self.context = context
        self.localcontext.update({
            'time': time,
            'cr':   cr,
            'uid':  uid,
        })


report_sxw.report_sxw('report.mmx_purchase_order_line', 'sale.order.line', 'extra_addons/mmx_purchase_qty/report/purchase_order_line.mako', parser=sale_order_line,)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: