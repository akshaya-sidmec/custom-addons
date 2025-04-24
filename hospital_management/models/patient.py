from odoo import models,fields,api
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    # _description = 'Patient Master'
    
    _rec_name = "doctor_id"
    _inherit = ['mail.thread','mail.activity.mixin']


    ref=fields.Char(string="Ref_ID",default="New")
    # doctor_id=fields.Many2one('hospital.doctor',String="name",required=True,tracking=True,domain=[('gender_doctor',"=",'Female')])
    doctor_id=fields.Many2one('hospital.doctor',String="name",required=True,tracking=True)
    name = fields.Char(String="Name",required=True)
    age =fields.Integer(String="Age")
    email = fields.Char(string="email")
    is_patient_in_ward = fields.Boolean("is patient in ward")
    admit_date = fields.Date("Admit date")
    discharge_date = fields.Date("discharge Date")
    gender=fields.Selection(String="Gender",selection=[('Male','M'),('Female','F')])
    gender_doctor= fields.Selection(String="Gender_doctor", selection=[('Male', 'M'), ('Female', 'F')])
    # gender_doctor = fields.Selection(related="doctor_id.gender_doctor",String="Gender_doctor", selection=[('Male', 'M'), ('Female', 'F')])
    patient_lines=fields.One2many('hospital.lines','patient','order lines')
    status=fields.Selection([("admit", "Admitted"), ("discharge", "Discharged")], "status", default='admit',compute="status_date")
    # status = fields.Selection([("admit", "Admitted"), ("discharge", "Discharged")], "status", default='admit')
    image=fields.Binary("image")
    patients = fields.Many2many('hospital.appointment', string="Patients")
    user_id = fields.Many2one("res.users", "user", compute="compute_user_company")
    company_id = fields.Many2one("res.company", "Company", compute="compute_user_company")
    sequence=fields.Integer(default=0)


    @api.model_create_multi #inheriting method
    def create(self, vals_list): # it automatically create a record in db
        for i in vals_list:
            if not i.get('ref') or i['ref']=='New':
                i['ref']=self.env['ir.sequence'].next_by_code('hospital.patient')
        """ We don't want the current user to be follower of all created job """
        return super().create(vals_list)

    def compute_user_company(self):
        for rec in self:
            rec.user_id = self.env.user
            rec.company_id = self.env.user.company_id.id

    @api.onchange("doctor_id")
    def onchange_doctor_name(self):
        for i in self:
            i.gender_doctor = i.doctor_id.gender_doctor

    def send_email(self):
        for rec in self:
            template = self.env.ref("hospital_management.mail_template_email_template")
            template.send_mail(rec.id, force_send=True)


    def status_date(self):
        today = date.today()
        for i in self :
            if i.discharge_date and today > i.discharge_date and i.admit_date < i.discharge_date:
                i.status='discharge'
            else:
                i.status='admit'

    def view_patient_lines(self):
        self.ensure_one()
        return {
            'name': "view patient invoices",
            'view_mode': 'list',
            'res_model': 'hospital.lines',
            'domain': [('patient', '=', self.id)],
            'type': 'ir.actions.act_window',
        }




class HospitalLines(models.Model):
    _name = 'hospital.lines'

    product_id = fields.Many2one("product.product", "product Name")
    qty = fields.Integer("qty")
    unit_price = fields.Float("unit_price",compute="compute_lines")
    patient = fields.Many2one("hospital.patient", "patient")
    sub_total = fields.Float(String="Sub_Total",compute="subtotal")


    def subtotal(self):
        for i in self:
            i.sub_total =i.unit_price*i.qty

    def compute_lines(self):
        for i in self:
            i.unit_price = i.product_id.standard_price
