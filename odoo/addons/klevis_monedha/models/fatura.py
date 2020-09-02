from odoo import fields, models, api


class KlevisFatura(models.Model):
    _inherit = 'klevis.fatura'

    monedha = fields.Many2one(comodel_name='klevis.monedha', string='Monedha')
    totali_lek = fields.Float(string='Totali ne lek (nese zgjidhet monedhe tjeter)')
    per_te_paguar_lek = fields.Float(string='Pagesa e bere ne Lek')

    @api.multi
    @api.depends('shporta_ids')
    def _llogarit_totalin(self):
        for obj in self:
            obj.totali = 0
            for shporte in obj.shporta_ids:
                obj.totali += shporte.totali

    @api.multi
    @api.depends('dhene_ne_dore', 'per_te_paguar')
    def _llogarit_kusurin(self):
        for obj in self:
            if obj.dhene_ne_dore > 0:
                obj.kusuri = abs(obj.per_te_paguar - obj.dhene_ne_dore)

    @api.multi
    @api.depends('totali', 'klienti')
    def _llogarit_uljen(self):
        for obj in self:
            obj.ulja = obj.totali * (obj.klienti.anetarsimi.ulja_perqindja / 100)

    @api.multi
    @api.depends('ulja', 'totali')
    def _per_te_paguar(self):
        for obj in self:
            obj.per_te_paguar = obj.totali - obj.ulja

    @api.multi
    @api.depends('per_te_paguar')
    def _llogarit_piket(self):
        for obj in self:
            obj.pike_shtuar = 0
            if obj.per_te_paguar <= 1000:
                obj.pike_shtuar += obj.per_te_paguar * 0.1
            elif obj.per_te_paguar <= 5000:
                obj.pike_shtuar += obj.per_te_paguar * 0.15
            else:
                obj.pike_shtuar += obj.per_te_paguar * 0.2
