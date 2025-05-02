from itertools import product
from odoo import models, fields
from odoo.addons.test_new_api.tests.test_one2many import One2manyCase
from odoo.fields import Many2many
from odoo.exceptions import UserError

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment Master'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, tracking=True)
    date = fields.Datetime(String="Date")
    gender = fields.Selection(String="Gender", selection=[('Male', 'M'), ('Female', 'F')])
    pat_lines = fields.One2many("hospital.appointment.lines", "p_name", "pat1_lines")
    status1 = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], default="draft", tracking=True,
                               compute="confirm")

    # def confirm(self):
    #     for i in self:
    #         i.status1='confirm'

    def send_mail(self):
        for rec in self:
            template = self.env.ref("hospital_management.mail_template_email_template")
            template.send_mail(rec.id, force_send=True)

    def confirm(self):
        for rec in self:
            # Check for existing patient by name (corrected condition)
            patient = self.env["hospital.patient"].search([('name', '=', rec.name)])
            if patient:
                raise UserError("Patient with this name already exists.")
            else:
                vals = {
                    'name': rec.name,
                    'patient_lines': [(0, 0, {
                        'prod_id': line.prod_id.id,
                        'tot_items': line.tot_items,
                        'prize': line.prize,
                        'tot': line.tot,
                    }) for line in rec.pat_lines]
                }
                self.env["hospital.patient"].create(vals)
                rec.status1 = "confirm"


class AppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'

    prod_id = fields.Many2one(comodel_name="product.product", string="Products")
    tot_items = fields.Integer("Quantity")
    prize = fields.Integer("Unit_price",compute="compute_lines")
    tot = fields.Integer("Total", compute="total")
    p_name = fields.Many2one("hospital.appointment", "Name")

    def total(self):
        for i in self:
            i.tot = i.tot_items * i.prize

    def compute_lines(self):
        for i in self:
            i.prize = i.prod_id.standard_price