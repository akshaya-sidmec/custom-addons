from odoo import fields, models, _


class PatientReport(models.TransientModel):
    _name = 'patient.invoices.wizard'
    _description = 'patient invoices report'

    name = fields.Char(String="Name")
    admit_date = fields.Date("Admit Date")
    discharge_date = fields.Date("Discharge Date")

    def view_pdf_report(self):
        return self.env.ref('hospital_management.report_patient_report_document').report_action(self)
       # for i in self:
       #     print(i)
       #  self.ensure_one()
       #  return {
       #      'name': "view_pdf_report  ",
       #      'view_mode': 'list',
       #      'res_model': 'hospital.lines',
       #      'domain': [('patient', '=', self.id)],
       #      'type': 'ir.actions.act_window',
       #  }
