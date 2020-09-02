from odoo import fields, models, api


class KlevisShporta(models.Model):
    _inherit = 'klevis.shporta'

    magazina_id = fields.Many2one(comodel_name='klevis.magazina', string='Magazina_id')
    sasia_ne_mag = fields.Float(string='Sasia ne magazine', compute='')
    sasia_id = fields.Many2one('klevis.sasia', compute='gjej_sasia_id', store=True)

    @api.multi
    @api.depends('magazina_id', 'produkti')
    def gjej_sasia_id(self):
        for shporta in self:
            shporta.sasia_id = self.env['klevis.sasia'].search([('produkt_id', '=', self.produkti.id), ('magazina_id', '=', self.magazina_id.id)], limit=1).id

    def llogarit(self):
        self.sasia_id.sasia += 10

