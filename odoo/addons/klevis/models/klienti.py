from odoo import fields, models, api


class KlevisKlienti (models.Model):
    _name = 'klevis.klienti'
    _description = 'Description'

    name = fields.Char(string='Name', required=True)
    mbiemer = fields.Char(string='Mbiemer', required=True)
    anetarsimi = fields.Many2one(comodel_name='klevis.anetarsimi', compute='_llogarit_antarsimin', string='Anetarsimi')
    piket = fields.Float(string='Piket', required=True, default=0)
    piket_shpenzuar = fields.Float(string='Piket_shpenzuar', required=True, default=0)

    fatura_ids = fields.One2many(comodel_name='klevis.fatura', inverse_name='klienti', string='Faturat')

    @api.multi
    @api.depends('piket', 'piket_shpenzuar')
    def _llogarit_antarsimin(self):
        for klienti in self:
            klienti.anetarsimi = self.env['klevis.anetarsimi'].search([('piket', '<=', (klienti.piket + klienti.piket_shpenzuar))], order='piket desc', limit=1).id


class KlevisAnetarsimi(models.Model):
    _name = 'klevis.anetarsimi'
    _description = 'Llojet e anetarsimeve'

    name = fields.Char(string='Name', required=True)
    ulja_perqindja = fields.Float(string='Perqindja e uljes', required=False)
    piket = fields.Float(string='Piket', required=False)

    klientet = fields.One2many(comodel_name='klevis.klienti', inverse_name='anetarsimi', string='Klientet', required=False)



