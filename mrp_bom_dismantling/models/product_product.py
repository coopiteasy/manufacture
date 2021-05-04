# © 2017 Eficent Business and IT Consulting Services S.L.
# © 2016 Cyril Gaudin (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import Counter
from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_view_bom(self):
        """ Override parent method to add a domain which filter out
        dismantling BoM
        """
        result = super(ProductProduct, self).action_view_bom()
        result['domain'] = [('dismantling', '=', False)]
        return result

    def _get_component_needs(self, product, bom):
        """ Return the needed qty of each compoments in the *bom* of *product*.

        :type product: product_product
        :type bom: mrp_bom
        :rtype: collections.Counter
        """
        needs = Counter()
        exploded_boms, exploded_lines = bom.explode(product, 1.0)

        for line, line_data in exploded_lines:
            product_id = line.product_id
            product_uom_id = line.product_uom_id
            qty = line_data['qty']
            component_qty = product_uom_id._compute_quantity(
                qty,
                product_id.uom_id,
            )
            needs += Counter(
                {product_id: component_qty}
            )
        return needs
