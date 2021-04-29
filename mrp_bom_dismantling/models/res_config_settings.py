# © 2016 Cyril Gaudin (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """ Add settings for dismantling BOM.
    """
    _inherit = 'res.config.settings'

    dismantling_product_choice = fields.Selection([
        (0, "Main BOM product will be set randomly"),
        (1, "User have to choose which component to set as main BOM product")
    ], "Dismantling BOM")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(dismantling_product_choice=self.env[
            'ir.config_parameter'].sudo().get_param(
            'mrp.bom.dismantling.product_choice',
            default=0)
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'mrp.bom.dismantling.product_choice', self.dismantling_product_choice)
