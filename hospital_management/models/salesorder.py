from odoo import fields,models

class SalesOrder(models.Model):
    _inherit = "sale.order"

    customer_address=fields.Char(string="Address")