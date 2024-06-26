from odoo import fields, models, api
from odoo.exceptions import Warning


class KlevisShporta(models.Model):
    _name = 'klevis.shporta'
    _description = 'Description'

    fatura = fields.Many2one(comodel_name='klevis.fatura', string='Fatura', ondelete="cascade")
    produkti = fields.Many2one(comodel_name='klevis.produkti', string='Produkti')
    sasia = fields.Float(string='Sasia', default=1)
    cmimi = fields.Float(string='Cmimi')
    totali = fields.Float(string='Totali', compute="_llogarit_totalin")

    @api.multi
    @api.depends('sasia', 'cmimi')
    def _llogarit_totalin(self):
        for shport in self:
            if shport.cmimi == 0:
                shport.cmimi = shport.produkti.cmimi
                shport.totali = shport.sasia * shport.produkti.cmimi
            else:
                shport.totali = shport.sasia * shport.cmimi

    @api.onchange('sasia', 'produkti')
    def _llogarit_kursin(self):
        self.cmimi = self.produkti.cmimi

    @api.model
    def create(self, values):
        if self._context.get('inherited_mag'):
            return super(KlevisShporta, self).create(values)
        else:
            res = super(KlevisShporta, self).create(values)
            if values.get('sasia') > res.produkti.sasia_ne_gjendje or values.get('sasia') <= 0:
                raise Warning('Kontrollo sasine qe kerkohet te blihet per produktin {}'.format(res.produkti.name))
            else:
                res.produkti.sasia_ne_gjendje = res.produkti.sasia_ne_gjendje - values.get('sasia')
            return res

    @api.multi
    def write(self, vals):
        for shporte in self:
            if shporte._context.get('inherited_mag'):
                return super(KlevisShporta, shporte).write(vals)
            else:
                if vals.get('sasia') > shporte.produkti.sasia_ne_gjendje or vals.get('sasia') <= 0 or not vals.get('sasia'):
                    raise Warning('Kontrollo sasine qe kerkohet te blihet per produktin {}'.format(shporte.produkti.name))
                else:
                    shporte.produkti.sasia_ne_gjendje = shporte.produkti.sasia_ne_gjendje - vals.get('sasia') + shporte.sasia
                return super(KlevisShporta, shporte).write(vals)

    @api.multi
    def unlink(self):
        for shporte in self:
            if shporte._context.get('inherited_mag'):
                return super(KlevisShporta, shporte).unlink()
            else:
                shporte.produkti.sasia_ne_gjendje += shporte.sasia
                return super(KlevisShporta, shporte).unlink()
