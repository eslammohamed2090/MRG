# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from num2words import num2words
from odoo import models, fields, api


class account_voucher(models.Model):
    _inherit = 'account.payment'

    @api.model
    def _get_check_formate(self):
        company_id = self.env.user.company_id.id
        formate_id = self.env['cheque.setting'].search([('set_default', '=', True), ('company_id', '=', company_id)],
                                                       limit=1)
        return formate_id.id

    cheque_formate_id = fields.Many2one('cheque.setting', 'Cheque Formate', default=_get_check_formate)
    cheque_no = fields.Char('Cheque No')
    text_free = fields.Char('Free Text')
    partner_text = fields.Char('Partner Title')

    def get_partner_name(self):
        if self.cheque_formate_id.partner_text and self.partner_text:
            if self.cheque_formate_id.partner_text == 'prefix':
                return self.partner_text + ' ' + self.partner_id.name
            else:
                return self.partner_id.name + ' ' + self.partner_text

        return self.partner_id.name

    def amount_word(self):
        amt = str(self.amount)
        amt_lst = amt.split('.')
        if self.partner_id and self.partner_id.lang:
            amt_word = num2words(int(amt_lst[0]), lang=self.partner_id.lang)
        else:
            amt_word = num2words(int(amt_lst[0]))
        lst = amt_word.split(' ')
        if float(amt_lst[1]) > 0:
            lst.append(' and ' + amt_lst[1] + ' / ' + str(100))
        lst.append('only')
        lst_len = len(lst)
        lst_len = len(lst)
        first_line = ''
        second_line = ''
        for l in range(0, lst_len):
            if lst[l] != 'euro':
                if self.cheque_formate_id.word_in_f_line >= l:
                    if first_line:
                        first_line = first_line + ' ' + lst[l]
                    else:
                        first_line = lst[l]
                else:
                    if second_line:
                        second_line = second_line + ' ' + lst[l]
                    else:
                        second_line = lst[l]

        if self.cheque_formate_id.is_star_word:
            first_line = '***' + first_line
            if second_line:
                second_line += '***'
            else:
                first_line = first_line + '***'

        first_line = first_line.replace(",", "")
        second_line = second_line.replace(",", "")
        return [first_line, second_line]

# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:
