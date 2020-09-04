from odoo import fields, models, api


class KlevisMagazina(models.Model):
    _name = 'klevismagazin.magazina'

    name = fields.Char(string='Emri', required=True)
    adresa = fields.Char(string='Adresa', required=False)
    produkt_ids = fields.One2many(comodel_name='klevismagazin.sasia', inverse_name='magazine_id', string='Produkt_ids', required=False)
