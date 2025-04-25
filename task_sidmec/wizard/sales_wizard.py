# from odoo import fields, models
#
#
# class CustomerReport(models.TransientModel):
#     _name = 'sales.wizard'
#     _description = 'Salesman Report'
#
#     salesperson = fields.Many2one("res.partner", String="Salesman")
#     from_date = fields.Date(String="From_date")
#     to_date = fields.Date(String="to_date")
#
#     def view_salesman_report(self):
#         rec = self  # or self.ensure_one() to be safer
#         partner = self.env['sale.order'].search([('partner_id', '=', rec.salesperson.id)])
#         data = {
#             'sale_order': partner
#         }
#         report_action = self.env.ref('task_sidmec.report_salesman')
#         return report_action.report_action(self, data=data)
from odoo import models, fields


class SaleOrderWizard(models.TransientModel):
    _name = "sale.report.wizard"
    _description = "Sale Report Wizard"

    partner_id = fields.Many2one("res.partner", string="Salesman")
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")

    def sale_pdf_report(self):
        for rec in self:
            domain = [('partner_id', '=', rec.partner_id.id)]

            if rec.from_date:
                domain.append(('date_order', '>=', rec.from_date))
            if rec.to_date:
                domain.append(('date_order', '<=', rec.to_date))

            sale_orders = self.env["sale.order"].search(domain, limit=10, order='date_order desc')

            total_amount = sum(order.amount_total for order in sale_orders)

            data = {
                'sale_orders': [
                    {
                        'name': order.name,
                        'amount_total': order.amount_total,
                        'sales_person': order.user_id.name,
                    }
                    for order in sale_orders
                ],
                'wizard': {
                    'partner_name': rec.partner_id.name,
                    'from_date': rec.from_date,
                    'to_date': rec.to_date,
                    'total_amount': total_amount,
                }
            }

            return self.env.ref('task_sidmec.sale_wizard_report_pdf').report_action(self, data=data)
