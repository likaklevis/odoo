from odoo import fields, models, api


class KlevisProdukti (models.Model):
    _name = 'klevis.produkti'
    _description = 'Description'

    name = fields.Char(string='Emri', required=True)
    cmimi = fields.Float(string='Cmimi', required=False)
    sasia_ne_gjendje = fields.Float(string='Sasia ne gjendje', required=False)
    vendodhja = fields.Char(string='Vendodhja', required=False)
    shporta_ids = fields.One2many(comodel_name='klevis.shporta', inverse_name='produkti', string='Shporta_ids', required=False)



