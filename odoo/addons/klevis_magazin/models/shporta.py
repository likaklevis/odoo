from odoo import fields, models, api


class KlevisShporta(models.Model):
    _inherit = 'klevis.shporta'

    magazina = fields.Many2one(comodel_name='klevis.magazina', string='Magazina', required=True)
    sasia_ne_mag = fields.Float(string='Sasia ne magazine', compute='')

