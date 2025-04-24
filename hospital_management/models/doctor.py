from odoo import models,fields

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(String="Name",required=True)
    experience =fields.Integer(String="Experience")
    gender_doctor=fields.Selection(String="Gender_doctor",selection=[('Male','M'),('Female','F')])
    patients=fields.Many2many('hospital.appointment',string="Patients")
