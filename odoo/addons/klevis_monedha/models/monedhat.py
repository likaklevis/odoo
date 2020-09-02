from odoo import fields, models, api
import requests


class KlevisMonedha(models.Model):
    _name = 'klevis.monedha'

    name = fields.Char(string='Monedha', required=True)
    simboli = fields.Char(string='Simboli', required=True)
    kursi_kembimit = fields.Float(string='Kursi kembimit', required=False)

    def kursi_ditor(self):
        search = self.env['klevis.monedha'].search([])
        for monedha in search:
            api_key = 'bcf2ed045befebbfc604'
            query = 'ALL_{}'.format(monedha.simboli)
            url = 'https://free.currconv.com/api/v7/convert?apiKey={}&q={}&compact=ultra'.format(api_key, query)
            vlera = requests.get(url).json()
            monedha.kursi_kembimit = vlera[query]

    @api.model
    def create(self, vals):
        api_key = 'bcf2ed045befebbfc604'
        query = 'ALL_{}'.format(self.simboli)
        url = 'https://free.currconv.com/api/v7/convert?apiKey={}&q={}&compact=ultra'.format(api_key, query)

        vlera = requests.get(url).json()
        if type(vlera.get(query)) is float:
            self.kursi_kembimit = vlera[query]
        else:
            raise Warning('Kontrollo simbolin e monedhes')

