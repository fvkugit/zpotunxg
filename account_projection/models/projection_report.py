from odoo import fields, models


class ProjectionReport(models.Model):
    """Configuration for projection XLSX report."""

    _name = 'account.projection.report'
    _description = 'Projection Report Configuration'

    name = fields.Char(required=True)
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, required=True
    )
    account_ids = fields.Many2many('account.account', string='Accounts')

    def action_print_xlsx(self):
        """Generate the projection report in XLSX format."""
        return self.env.ref(
            'account_projection.action_projection_report_xlsx'
        ).report_action(self)
