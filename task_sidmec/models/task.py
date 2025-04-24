from odoo import fields,models,api
import re
from odoo.exceptions import  ValidationError
from datetime import date,datetime

class CustomerForm(models.Model):
    _inherit = "res.partner"

    cust_id = fields.Char("Cust_ID", tracking=True, default='New')
    gst_no=fields.Char(String="GST_Number")
    dob=fields.Date("Date_of_Birth")
    age=fields.Integer("Age",compute="Dob")


    def Dob(self):

        for i in self:
            if i.dob:
                i.age = date.today().year - i.dob.year
                #date.today() gives current day
            else:
                i.age=0

    @api.constrains('gst_no')
    def gst_number(self):
        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'

        for i in self:
            if i.gst_no:
                if len(i.gst_no) != 15 or not re.match(gst_pattern,i.gst_no):
                # if len(i.gst_no) != 15 or i.gst_no != gst_pattern:
                    raise ValidationError("Invalid GST Number")

    @api.model_create_multi  # inheriting method
    def create(self, k):  # it automatically create a record in db
        for i in k:
            if not i.get('cust_id') or i['cust_id'] == 'New':
                i['cust_id'] = self.env['ir.sequence'].next_by_code('res.partner')
        return super().create(k)


