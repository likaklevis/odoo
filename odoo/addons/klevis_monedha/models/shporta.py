from odoo import fields, models, api


class KlevisShporta (models.Model):
    _inherit = 'klevis.shporta'

    @api.multi
    @api.depends('sasia', 'cmimi')
    def _llogarit_totalin(self):
        for shport in self:
            shport.totali = shport.sasia * shport.cmimi

    @api.onchange('sasia', 'produkti', 'fatura')
    def _llogarit_kursin(self):
        self.cmimi = self.produkti.cmimi * self.fatura.monedha.kursi_kembimit



