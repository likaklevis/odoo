from odoo import fields, models, api
import requests


class KlevisMonedha(models.Model):
    _name = 'klevismonedha.monedha'

    name = fields.Char(string='Monedha', required=True)
    simboli = fields.Char(string='Simboli', required=True)
    kursi_kembimit = fields.Float(string='Kursi kembimit', required=False, digits=(12, 5))
    data_perditesuar = fields.Datetime(string='Perditesuar', required=False)

    def kursi_ditor(self):
        search = self.env['klevismonedha.monedha'].search([])
        for monedha in search:
            api_key = 'bcf2ed045befebbfc604'
            self.simboli = self.simboli.upper()
            query = 'ALL_{}'.format(self.simboli)
            url = 'https://free.currconv.com/api/v7/convert?apiKey={}&q={}&compact=ultra'.format(api_key, query)
            vlera = requests.get(url).json()
            monedha.kursi_kembimit = vlera.get(query)
            monedha.data_perditesuar = fields.datetime.now()

    @api.model
    def create(self, values):
        res = super(KlevisMonedha, self).create(values)
        api_key = 'bcf2ed045befebbfc604'
        res.simboli = res.simboli.upper()
        query = 'ALL_{}'.format(res.simboli)
        url = 'https://free.currconv.com/api/v7/convert?apiKey={}&q={}&compact=ultra'.format(api_key, query)
        vlera = requests.get(url).json()
        if vlera.get(query) and type(vlera.get(query)) is float or type(vlera.get(query)) is int:
            res.kursi_kembimit = vlera.get(query)
            res.data_perditesuar = fields.datetime.now()
        else:
            raise Warning('Kontrollo simbolin e monedhes/API')
        return res
