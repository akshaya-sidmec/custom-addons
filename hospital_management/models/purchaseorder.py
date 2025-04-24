from odoo import fields,models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase=fields.Integer(String="Purchase number")