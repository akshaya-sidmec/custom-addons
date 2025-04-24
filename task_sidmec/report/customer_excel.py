from odoo import models,fields


class PartnerXlsxReport(models.AbstractModel):
    _name = "report.task_sidmec.report_customer_excel"
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, k):
        print('lines:',k.name)
        format1 = workbook.add_format({'font_size': 14, 'bold': True})
        format2 = workbook.add_format({'font_size': 10})
        sheet=workbook.add_worksheet('customer Card')
        sheet.write(2,2,'Name',format1)
        sheet.write(2,3,k.name,format2)
        sheet.write(3, 2, 'Age', format1)
        sheet.write(3, 3, k.age, format2) #row,col