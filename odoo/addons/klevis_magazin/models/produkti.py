from odoo import fields, models, api


class KlevisProdukti (models.Model):
    _inherit = 'klevis.produkti'

    magazina_id = fields.Many2many(comodel_name='klevis.magazina', relation='produkti_mag_rel', column1='produkt_id', column2='mag_id', string='Magazinat')


class KlevisSasia (models.Model):
    _name = 'klevis.sasia'

