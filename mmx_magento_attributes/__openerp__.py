# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2013 Camptocamp SA
#    Copyright 2013 Akretion
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


{'name': 'Magento Connector - Catalog Attributes',
 'version': '7.0.1.0.6',
 'category': 'Connector',
 'depends': ['magentoerpconnect',
             'product_custom_attributes',
             'mmx_product',
             ],
 'author': 'MagentoERPconnect Core Editors',
 'license': 'AGPL-3',
 'website': 'https://launchpad.net/magentoerpconnect',
 'description': """
Magento Connector - Catalog
===========================

Extension for **Magento Connector**, add management of the product's catalog:

* product links
* product images
* export of products, categories, links and images

""",
    'images': ['images/jobs.png',
            'images/product_binding.png',
        ],
    'demo': [],
    'data': [
        'security/attribute_group_view.xml',
        'security/attribute_rule_view.xml',
        'security/ir.model.access.csv',
        'product_attribute_view.xml',
        'magento_model_view.xml',
        'product_scale_view.xml',
        # 'product_manufacturers_view.xml',
        'product_model_view.xml',
        'product_race_view.xml',
        'product_driver_view.xml',
    ],
    'installable': True,
    'application': False,
}
