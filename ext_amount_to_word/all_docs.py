# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import osv, fields
from openerp.tools.amount_to_text_en import amount_to_text
from amount_to_text_th import amount_to_text_th


class AmountToWord(object):

    def _get_amount_total(self, obj):
        amount_total = 0.0
        if obj._name in ('account.invoice', 'sale.order'): # Order, Invoice
            amount_total = obj.amount_total
        elif obj.name == 'account.voucher': 
            for cr_line in obj.line_cr_ids:
                amount_total += cr_line.amount
            for dr_line in obj.line_dr_ids:
                amount_total -= dr_line.amount
            amount_total = abs(amount_total)            
        return amount_total
    
    def _amount_to_word_en(self, cursor, user, ids, name, arg, context=None):
        res = {}
        minus = False
        amount_text = ''
        for obj in self.browse(cursor, user, ids, context=context):
            a = 'Baht'
            b = 'Satang'
            if obj.currency_id.name == 'JYP':
                a = 'Yen'
                b = 'Sen'
            if obj.currency_id.name == 'GBP':
                a = 'Pound'
                b = 'Penny'
            if obj.currency_id.name == 'USD':
                a = 'Dollar'
                b = 'Cent'
            if obj.currency_id.name == 'EUR':
                a = 'Euro'
                b = 'Cent'   
            amount_total = self._get_amount_total(obj)
            if amount_total < 0:
                minus = True
                amount_total = -amount_total
            amount_text = amount_to_text(amount_total, 'en', a).replace('and Zero Cent', 'Only').replace('Cent', b).replace('Cents', b)
            res[obj.id] = minus and 'Minus ' + amount_text or amount_text
        return res
    
    def _amount_to_word_th(self, cursor, user, ids, name, arg, context=None):
        res = {}
        minus = False
        amount_text = ''
        for obj in self.browse(cursor, user, ids, context=context):
            amount_total = self._get_amount_total(obj)
            if amount_total < 0:
                minus = True
                amount_total = -amount_total
            amount_text = amount_to_text_th(amount_total, obj.currency_id.name)
            res[obj.id] = minus and 'ลบ' + amount_text or amount_text
            
        return res

class account_invoice(AmountToWord, osv.osv):
    
    _inherit = 'account.invoice'

    def _get_invoice_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()

    def _get_invoice_tax(self, cr, uid, ids, context=None):
        result = {}
        for tax in self.pool.get('account.invoice.tax').browse(cr, uid, ids, context=context):
            result[tax.invoice_id.id] = True
        return result.keys()
    
    def _amount_total_text_en(self, cursor, user, ids, name, arg, context=None):   
        return self._amount_to_word_en(cursor, user, ids, name, arg, context=context)

    def _amount_total_text_th(self, cursor, user, ids, name, arg, context=None):   
        return self._amount_to_word_th(cursor, user, ids, name, arg, context=context)
    
    _columns = {
        'amount_total_text_en': fields.function(_amount_total_text_en, string='Amount Total (EN)', type='char',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
            }),
        'amount_total_text_th': fields.function(_amount_total_text_th, string='Amount Total (TH)', type='char',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
            }),
    }
    
class account_voucher(AmountToWord, osv.osv):
    
    _inherit = 'account.voucher'
    
    def _amount_total_text_en(self, cursor, user, ids, name, arg, context=None):   
        return self._amount_to_word_en(cursor, user, ids, name, arg, context=context)

    def _amount_total_text_th(self, cursor, user, ids, name, arg, context=None):   
        return self._amount_to_word_th(cursor, user, ids, name, arg, context=context)
    
    _columns = {
        'amount_total_text_en': fields.function(_amount_total_text_en, string='Amount Total (EN)', type='char',
            store={'account.voucher': (lambda self, cr, uid, ids, c={}: ids, ['line_cr_ids', 'line_dr_ids'], 100),}),
        'amount_total_text_th': fields.function(_amount_total_text_th, string='Amount Total (TH)', type='char',
            store={'account.voucher': (lambda self, cr, uid, ids, c={}: ids, ['line_cr_ids', 'line_dr_ids'], 100),}),
    }
    
class sale_order(AmountToWord, osv.osv):
    
    _inherit = 'sale.order'

    def _amount_total_text_en(self, cursor, user, ids, name, arg, context=None):   
        return self._amount_to_word_en(cursor, user, ids, name, arg, context=context)

    def _amount_total_text_th(self, cursor, user, ids, name, arg, context=None):   
        return self._amount_to_word_th(cursor, user, ids, name, arg, context=context)

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    _columns = {
        'amount_total_text_en': fields.function(_amount_total_text_en, string='Amount Total (EN)', type='char',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),
        'amount_total_text_th': fields.function(_amount_total_text_th, string='Amount Total (TH)', type='char',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),    
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
