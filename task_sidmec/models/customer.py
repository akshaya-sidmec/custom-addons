from odoo import models, fields,api
from datetime import date
from odoo.exceptions import ValidationError
import re
from odoo.osv import expression

class TaskCustomer(models.Model):
    _name = 'task.customer'
    _description = 'Customer Gst Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    cust_id = fields.Char("Cust_ID",tracking=True,default='New')
    partner_id=fields.Many2one("res.partner",string="PID")
    name=fields.Char("Customer",tracking=True,required=True)
    age=fields.Integer("Age",tracking=True,compute="compute_dob")
    dob=fields.Date("Date_of_birth")
    user_id=fields.Many2one("res.users","Users")
    company_id = fields.Many2one("res.company", "Company")
    email = fields.Char("Email")
    image=fields.Binary('Image')

    @api.model_create_multi #inheriting method
    def create(self,vals): # it automatically create a record in db
        for i in vals:
            if not i.get('cust_id') or i['cust_id']=='New':
                i['cust_id']=self.env['ir.sequence'].next_by_code('task.customer')
        return super().create(vals)

    def mail(self):#task1[23 apr]
        for i in self:
            temp=self.env.ref("task_sidmec.email_template")
            temp.send_mail(i.id,force_send=True)

    @api.onchange("user_id") #task2[23 apr]
    def onchange_user(self):
        for i in self:
            i.email=i.user_id.email

    def compute_dob(self):#task3[23 apr]
        for i in self:
            if i.dob:
                i.age=date.today().year-i.dob.year
            else:
                i.age=0

    @api.constrains('name')#task4[23 apr]
    def name_condition(self):
        name_ptrn=r'^[A-Z][a-z]+$'
        for i in self:
            if i.name:
                if len(i.name)<3 or not re.match(name_ptrn,i.name):
                    raise ValidationError("Only one word that start with  upper and followed by lower are allowed EX:Akshaya")

    class ResPartner(models.Model): #task5[23 apr]
        _inherit = 'res.partner'

        @api.model
        def name_search(self, name='', args=None, operator='ilike', limit=100):
            args = []
            domain = []
            if name:
                domain = expression.OR([
                    [('name', operator, name)],
                    [('phone', operator, name)],
                    [('email', operator, name)],
                ])
            records = self.search(expression.AND([args, domain]), limit=limit)
            return [(rec.id, f"{rec.name}") for rec in self.browse(records.ids)]

class Accounting(models.Model):
    _inherit = "account.move"



