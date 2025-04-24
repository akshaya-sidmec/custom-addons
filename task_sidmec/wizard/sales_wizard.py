from odoo import fields, models


class CustomerReport(models.TransientModel):
    _name = 'sales.wizard'
    _description = 'Salesman Report'

    salesperson = fields.Many2one("res.partner", String="Salesman")
    from_date = fields.Date(String="From_date")
    to_date = fields.Date(String="to_date")

    def view_salesman_report(self):
        for rec in self:
            partner = self.env['sale.order'].search([('partner_id', '=', rec.salesperson.id)])
            data = {
                'sale_order': partner
            }
        #     print(data)
            report_action = self.env.ref('task_sidmec.report_salesman')  # Change to the correct report action
            return report_action.report_action(self,data=data)
