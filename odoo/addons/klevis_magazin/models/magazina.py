from odoo import fields, models, api


class KlevisMagazina (models.Model):
    _name = 'klevis.magazina'

    name = fields.Char(string='Emri')
    adresa = fields.Char(string='Adresa')



