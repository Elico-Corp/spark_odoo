# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#    Author: Jon chow <jon.chow@elico-corp.com>
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

{
    'name': 'SOL order by onhand qty',
    'version': '1.0',
    'author': 'Elico Corp',
    'website': 'http://www.elico-corp.com',
    'summary': '',
    'description': """
         SOL order by onhand qty
    """,
    'depends': ['base', 'sale_order_line'],
    'category': '',
    'sequence': 10,
    'demo': [],
    'data': [
        'wizard/sol_sort_onhand_qty_view.xml',
        # 'security/ir.model.access.csv',
        ],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'css': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
