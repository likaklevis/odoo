from odoo import fields, models, api
from odoo.exceptions import UserError


class KlevisShporta(models.Model):
    _inherit = 'klevis.shporta'

    magazina_id = fields.Many2one(comodel_name='klevismagazin.magazina', string='Magazina_id', required=True)
    sasia_id = fields.Many2one('klevismagazin.sasia', compute='gjej_sasia_id', store=True)

    @api.multi
    @api.depends('magazina_id', 'produkti')
    def gjej_sasia_id(self):
        for shporta in self:
            if shporta.magazina_id:
                sasia_id = self.env['klevismagazin.sasia'].search([('produkt_id', '=', shporta.produkti.id), ('magazine_id', '=', shporta.magazina_id.id), ('sasia', '>', 0)], limit=1)
                if sasia_id:
                    shporta.sasia_id = sasia_id.id

    @api.model
    def create(self, values):
        ctx = self._context.copy()
        ctx['inherited_mag'] = True
        res = super(KlevisShporta, self.with_context(ctx)).create(values)
        if values.get('sasia') > res.sasia_id.sasia or values.get('sasia') <= 0:
            listmag = []
            search = self.env['klevismagazin.sasia'].search([('produkt_id', '=', res.produkti.id), ('sasia', '>=', res.sasia)])
            if search:
                for obj in search:
                    listmag.append(obj.magazina_id.name)
                magazinat_lira = ', '.join(listmag)
                raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Magazinat qe suportojn sasine e caktuar: '.format(res.produkti.name, res.magazina_id.name, magazinat_lira))
            else:
                raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Asnje magazine nuk e suporton dot sasine e kerkuar.'.format(res.produkti.name, res.magazina_id.name))
        else:
            res.sasia_id.sasia = res.sasia_id.sasia - values.get('sasia')
        return res

    @api.multi
    def write(self, vals):
        for shporte in self:
            ctx = shporte._context.copy()
            ctx['inherited_mag'] = True
            print(shporte.sasia_id.sasia)
            print(vals.get('sasia'))
            if vals.get('sasia') > shporte.sasia_id.sasia or vals.get('sasia') <= 0 or not vals.get('sasia'):
                listmag = []
                search = self.env['klevismagazin.sasia'].search([('produkt_id', '=', shporte.produkti.id), ('sasia', '>=', shporte.sasia)])
                if search and vals.get('sasia') > shporte.sasia_id.sasia:
                    for obj in search:
                        listmag.append(obj.magazine_id.name)
                    magazinat_lira = ', '.join(listmag)
                    print(shporte.sasia_id.sasia)
                    raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Magazinat qe suportojn sasine e caktuar: '.format(shporte.produkti.name, shporte.magazina_id.name, magazinat_lira))
                else:
                    raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Asnje magazine nuk e suporton dot sasine e kerkuar.'.format(shporte.produkti.name, shporte.magazina_id.name))
            else:
                shporte.sasia_id.sasia = shporte.sasia_id.sasia - vals.get('sasia') + shporte.sasia
            return super(KlevisShporta, shporte.with_context(ctx)).write(vals)

    @api.multi
    def unlink(self):
        for shporte in self:
            ctx = shporte._context.copy()
            ctx['inherited_mag'] = True
            shporte.sasia_id.sasia += shporte.sasia
            return super(KlevisShporta, shporte.with_context(ctx)).unlink()
