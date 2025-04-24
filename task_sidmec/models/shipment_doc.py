from odoo import models, fields,api
from odoo.exceptions import ValidationError,UserError


class ShipmentDocument(models.Model):
    _name = 'shipment.document'
    _description = 'Shipment Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    doc_id = fields.Char("Doc_ID",tracking=True,default='New')
    name=fields.Char("Customer",tracking=True,required=True)

    pdf=fields.Binary("Upload_PDF",tracking=True,attachment=True)
    filename = fields.Char(string='Filename', required=True)
    status = fields.Selection([("draft", "Draft"), ("completed", "Completed")], "status", default='draft',compute="compute_state")

    @api.constrains('filename')
    def _check_pdf_extension(self):
        for rec in self:
            if rec.filename and not rec.filename.lower().endswith('.pdf'):
                raise ValidationError("Only PDF files are allowed")

    def compute_state(self):
        for i in self :
            if i.pdf:
                i.status="completed"
            else:
                i.status="draft"

    def unlink(self):
        for rec in self:
            if rec.status == 'completed':
                raise UserError("You cannot delete documents linked to a completed shipment.")
        return super().unlink()


    @api.model_create_multi #inheriting method
    def create(self,k): # it automatically create a record in db
        for i in k:
            if not i.get('doc_id') or i['doc_id']=='New':
                i['doc_id']=self.env['ir.sequence'].next_by_code('shipment.document')
        return super().create(k)


