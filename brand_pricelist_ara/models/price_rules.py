from odoo import _, api, fields, models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    display_applied_on = fields.Selection(
        selection_add=[("25_brand", "Brand")],
        ondelete={"25_brand": "set default"},
    )
    product_brand_id = fields.Many2one(
        "product.brand",
        string="Brand",
        ondelete="cascade",
    )

    @api.depends("applied_on", "categ_id", "product_tmpl_id", "product_id", "product_brand_id")
    def _compute_name(self):
        super()._compute_name()
        for item in self:
            if item.display_applied_on == "25_brand" and item.product_brand_id:
                item.name = _("Brand: %s", item.product_brand_id.name)

    def _is_applicable_for(self, product, qty_in_product_uom):
        self.ensure_one()
        # cek brand
        if qty_in_product_uom < self.min_quantity:
            return False
        if self.display_applied_on == "25_brand":
            return self.product_brand_id and product.product_tmpl_id.product_brand_id == self.product_brand_id
        return super()._is_applicable_for(product, qty_in_product_uom)

    @api.onchange("display_applied_on")
    def _onchange_display_applied_on(self):
        super()._onchange_display_applied_on()
        for item in self:
            if item.display_applied_on == "25_brand":
                item.update({
                    "applied_on": "3_global", 
                    "product_id": None,
                    "product_tmpl_id": None,
                    "categ_id": None,
                })
