from itertools import product

from odoo import models,fields
from odoo.addons.test_new_api.tests.test_one2many import One2manyCase
from odoo.fields import Many2many


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment Master'
    _inherit =['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Name",required=True,tracking=True)
    date =fields.Datetime(String="Date")
    gender=fields.Selection(String="Gender",selection=[('Male','M'),('Female','F')])
    pat_lines=fields.One2many("hospital.appointment.lines","p_name","pat1_lines")
    status1=fields.Selection([('draft','Draft'),('confirm','Confirmed')],default="draft",tracking=True,compute="confirm")
    def confirm(self):
        for i in self:
            if i.status1==i.confirm:
                i.status1='confirm'
            else:
                i.status1 = 'draft'
    def  send_mail(self):
        for rec in self:
            template = self.env.ref("hospital_management.mail_template_email_template")
            template.send_mail(rec.id, force_send=True)

    def status(self):
        pass

class AppointmentLines(models.Model):
    _name= 'hospital.appointment.lines'

    prod_id=fields.Many2one(comodel_name="product.product",string="Products")
    tot_items=fields.Integer("Quantity")
    prize=fields.Integer("Unit_price")
    tot=fields.Integer("Total",compute="total")
    p_name=fields.Many2one("hospital.appointment","Name")

    def total(self):
        for i in self:
            i.tot=i.tot_items * i.prize
