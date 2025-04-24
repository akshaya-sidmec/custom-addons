from odoo import models,fields,api
from datetime import date
class CustomerFollowup(models.Model):
    _name = 'customer.followup'
    _description = 'Customer_Follow_up'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "customer"

    customer=fields.Char("Customer")
    sales_person=fields.Many2one('res.users',"Sales_Person")
    follow_up=fields.Date("Follow_Up")


    @api.model
    def default_get(self, fields):
        res = super(CustomerFollowup, self).default_get(fields)
        if 'sales_person' in fields:
            res['sales_person'] = self.env.uid
        if 'follow_up' in fields:
            res['follow_up'] = date.today()
        return res
