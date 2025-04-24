from odoo import models, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def unlink(self):
        for i in self:
            if i.state not in ['draft', 'cancel']:
                raise UserError("You cannot delete confirmed Sales Orders")
        return super(SaleOrder, self).unlink()
