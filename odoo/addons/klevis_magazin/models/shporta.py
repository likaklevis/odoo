from odoo import fields, models, api


class KlevisShporta(models.Model):
    _inherit = 'klevis.shporta'

    magazina_id = fields.Many2one(comodel_name='klevismagazin.magazina', string='Magazina_id')
    sasia_id = fields.Many2one('klevismagazin.sasia', compute='gjej_sasia_id', store=True)

    @api.multi
    @api.depends('magazina_id', 'produkti')
    def gjej_sasia_id(self):
        for shporta in self:
            shporta.sasia_id = self.env['klevismagazin.sasia'].search([('produkt_id', '=', self.produkti.id), ('magazina_id', '=', self.magazina_id.id)], limit=1).id

    @api.model
    def create(self, values):
        ctx = self._context.copy()
        ctx['inherited_mag']