from odoo import fields, models, api


class KlevisFatura (models.Model):
    _inherit = 'klevis.fatura'

    @api.multi
    def unlink(self):
        for fature in self:
            ctx = fature._context.copy()
            ctx['inherited_mag'] = True
            for obj in fature.shporta_ids:
                obj.produkti.magazinat_ids.sasia += obj.sasia
            if fature.menyra_pageses == 'cash':
                fature.klienti.piket -= fature.pike_shtuar
            elif fature.menyra_pageses == 'pike':
                fature.klienti.piket_shpenzuar -= fature.pike_paguar
            return super(KlevisFatura, fature.with_context(ctx)).unlink()
    


