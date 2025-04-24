from odoo import fields, models, _


class CustomerReport(models.TransientModel):
    _name = 'customer.wizard'
    _description = 'customers report'

    name = fields.Char(String="Customer_Name")
    age= fields.Integer(String="Age")
    email= fields.Char(String="Email")

    def view_pdf_report(self):
        return self.env.ref('task_sidmec.report_customer_pdf').report_action(self)