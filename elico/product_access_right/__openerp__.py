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
    'name':         'Product Form View Visibility',
    'version':      '1.0',
    'author':       'Elico Corp',
    'website':      'http://www.elico-corp.com',
    'summary':      '',
    'description' : """This Module limits the visibility of Product form view
    Sale, purchase, warehouse info only visible by respective managers.
    """,
    'depends':      ['base','product','stock','sale','purchase','account'],
    'category':     '',
    'sequence':     10,
    'demo':         [],
    'data':         ['product_view.xml',],
    'test':         [],
    'installable':  True,
    'application':  False,
    'auto_install': False,
    'css':          [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: