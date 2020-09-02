from odoo import fields, models, api


class KlevisProdukti(models.Model):
    _inherit = 'klevis.produkti'


class KlevisSasia(models.Model):
    _name = 'klevis.sasia'

    produkt_id = fields.Many2one(comodel_name='klevis.produkti', string='Produkti', required=True)
    magazine_id = fields.Many2one(comodel_name='klevis.magazina', string='Magazine ID', required=True)
    sasia = fields.Float(string='Sasia', required=True)

    _sql_constraints = [('prod_mag_unique', 'unique (produkt_id, magazine_id)', 'ID e produktit te jet unik per magazine')]
