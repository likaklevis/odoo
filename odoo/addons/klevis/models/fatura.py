from odoo import fields, models, api


class KlevisFatura(models.Model):
    _name = 'klevis.fatura'
    _description = 'Description'

    name = fields.Char(string='Name')
    klienti = fields.Many2one(comodel_name='klevis.klienti', string='Klienti', default=0)
    totali = fields.Float(string='Totali', compute='_llogarit_totalin')
    menyra_pageses = fields.Selection(string='Menyra pageses', required=True,
                                      selection=[('pike', 'Me pike'),
                                                 ('cash', 'Para ne dore')])
    ulja = fields.Float(string='Ulja', compute='_llogarit_uljen')
    dhene_ne_dore = fields.Float(string='Dhene ne dore')
    per_te_paguar = fields.Float(string='Per te paguar', compute='_per_te_paguar')  # nese ka ulje
    kusuri = fields.Float(string='Kusuri', compute='_llogarit_kusurin')
    pike_shtuar = fields.Float(string='Pike shtuar', compute='_llogarit_piket')
    pike_paguar = fields.Float(string='Pike paguar')
    ora = fields.Datetime(string='Ora', required=False)
    shporta_ids = fields.One2many(comodel_name='klevis.shporta', inverse_name='fatura', string='Shporta_ids')

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

    @api.model
    def create(self, values):
        if self._context.get('inherited'):
            return super()
        else:
            res = super(KlevisFatura, self).create(values)
            res.ora = fields.datetime.now()
            res.name = "Fatura {}".format(res.id)
            if values.get('menyra_pageses') == 'cash':
                if res.dhene_ne_dore < res.per_te_paguar:
                    raise Warning('Vlera e dhene nuk mjafton per te kryer blerjen')
                res.klienti.piket += res.pike_shtuar
            elif values.get('menyra_pageses') == 'pike':
                if res.klienti.piket >= res.pike_paguar >= res.totali:
                    res.klienti.piket -= res.pike_paguar
                    res.klienti.piket_shpenzuar += res.pike_paguar
                else:
                    raise Warning('Piket nuk jan mjaftueshem')
            return res

    @api.multi
    def write(self, vals):
        for fature in self:
            if fature.menyra_pageses == 'cash':
                fature.klienti.piket -= fature.pike_shtuar
            elif fature.menyra_pageses == 'pike':
                fature.klienti.piket_shpenzuar -= fature.pike_paguar

            res = super(KlevisFatura, fature).write(vals)

            if fature.menyra_pageses == 'cash':
                if fature.dhene_ne_dore < fature.per_te_paguar:
                    raise Warning('Vlera e dhene nuk mjafton per te kryer blerjen')
                fature.klienti.piket += fature.pike_shtuar
            elif fature.menyra_pageses == 'pike':
                if fature.klienti.piket >= fature.pike_paguar >= fature.totali:
                    fature.klienti.piket -= fature.pike_paguar
                    fature.klienti.piket_shpenzuar += fature.pike_paguar
                else:
                    raise Warning('Piket nuk jan mjaftueshem')
            return res

    @api.multi
    def unlink(self):
        for fature in self:
            for obj in fature.shporta_ids:
                obj.produkti.sasia_ne_gjendje += obj.sasia
            if fature.menyra_pageses == 'cash':
                fature.klienti.piket -= fature.pike_shtuar
            elif fature.menyra_pageses == 'pike':
                fature.klienti.piket_shpenzuar -= fature.pike_paguar
            return super(KlevisFatura, fature).unlink()


