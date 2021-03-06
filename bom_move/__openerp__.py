# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Ecosoft Co., Ltd. (http://ecosoft.co.th).
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
    'name' : 'Bom Move (SQP)',
    'version' : '1.0',
    'author' : 'Ecosoft',
    'summary': 'Bom Move (SQP)',
    'description': """
This module reuse Delivery Order for Bom Move. Internally it is DO, marked with Product Category as 'Bom Move'
New 'Bom Move' menu will load Bom Move window, auto marked category as Bom Move.
All product created, must be in category Part (sqp_config.product_category_part).
* Enchance #1035
* *
* * * Remove saleorder_id name field for reference info from Sale Order.
* * * In the Supply List Form, show the Sale Order reference and hide Source Document when if supply list flag is true.
    """,
    'category': 'Warehouse Management',
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['web_m2o_enhanced','product', 'ext_mrp', 'hr', 'stock_supply_list'],
    'demo' : [],
    'data' : [
              'product_view.xml',
              'stock_view.xml',
              'stock_workflow.xml',
              'mrp_view.xml',
              'bom_move_sequence.xml',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
