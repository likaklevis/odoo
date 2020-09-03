from odoo import fields, models, api


class KlevisFatura(models.Model):
    _inherit = 'klevis.fatura'

    monedha = fields.Many2one(comodel_name='klevismonedha.monedha', string='Monedha', default=lambda self: self.env['klevismonedha.monedha'].search([], limit=1)) # default leku, first record
    kursi = fields.Float(string='Totali ne lek', compute='_llogarit_kursin')
    totali_lek = fields.Float(string='Totali ne lek')  # jo 0 nese zgjidhet monedhe tjeter
    per_te_paguar_lek = fields.Float(string='Pagesa e bere ne Lek')

    @api.multi
    @api.depends('shporta_ids', 'monedha')
    def _llogarit_totalin(self):
        for obj in self:
            obj.totali = 0
            for shporte in obj.shporta_ids:
                obj.totali += shporte.totali
            obj.totali = obj.totali * obj.monedha.kursi_kembimit

    @api.multi
    @api.depends('ulja', 'totali')
    def _per_te_paguar(self):
        for obj in self:
            obj.per_te_paguar = obj.totali - obj.ulja

    @api.multi
    @api.depends('dhene_ne_dore', 'per_te_paguar')
    def _llogarit_kusurin(self):
        for obj in self:
            if obj.dhene_ne_dore > 0:
                obj.kusuri = obj.per_te_paguar - obj.dhene_ne_dore

    @api.multi
    @api.depends('totali', 'klienti')
    def _llogarit_uljen(self):
        for obj in self:
            obj.ulja = obj.totali * (obj.klienti.anetarsimi.ulja_perqindja / 100)


    @api.multi
    @api.depends('per_te_paguar')
    def _llogarit_piket(self):
        for obj in self:
            obj.pike_shtuar = 0
            if obj.per_te_paguar <= 1000:
                obj.pike_shtuar += obj.per_te_paguar * 0.1 * obj.kursi
            elif obj.per_te_paguar <= 5000:
                obj.pike_shtuar += obj.per_te_paguar * 0.15 * obj.kursi
            else:
                obj.pike_shtuar += obj.per_te_paguar * 0.2 * obj.kursi

    @api.multi
    @api.depends('monedha')
    def _llogarit_kursin(self):
        for obj in self:
            if obj.monedha.kursi_kembimit:
                obj.kursi = 1/obj.monedha.kursi_kembimit

    @api.multi
    @api.depends('monedha', 'shporta_ids', 'kursi')
    def _llogarit_ne_lek(self):
        for obj in self:
            if obj.monedha.simboli != 'ALL':
                obj.per_te_paguar_lek = obj.per_te_paguar * obj.kursi
                obj.totali_lek = obj.totali * obj.kursi

    @api.model
    def create(self, values):
        return super(KlevisFatura, self).create(values)

    @api.multi
    def write(self, vals):
        for fature in self:
            return super(KlevisFatura, fature).write(vals)

    @api.multi
    def unlink(self):
        for fature in self:
            return super(KlevisFatura, fature).unlink()
