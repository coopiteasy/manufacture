# © 2016 Cyril Gaudin (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """ Add settings for dismantling BOM.
    """
    _inherit = 'res.config.settings'

    dismantling_product_choice = fields.Selection([
        ('random', "Main BOM product will be set randomly"),
        ('user', "User have to choose which component to set as main BOM product")
    ], default="random", string="Dismantling BOM", config_parameter='mrp.bom.dismantling.product_choice')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        dismantling_product_choice = ICPSudo.get_param('mrp.bom.dismantling.product_choice', default="random")
        res.update(
           dismantling_product_choice=dismantling_product_choice,
        )
        return res

    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('mrp.bom.dismantling.product_choice', self.dismantling_product_choice or "random")

