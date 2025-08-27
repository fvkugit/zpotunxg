from odoo import models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class ProjectionReportXlsx(ReportXlsx):
    """XLSX report for financial projections."""

    _name = 'report.account_projection.projection_report_xlsx'
    _description = 'Projection Report XLSX'

    def generate_xlsx_report(self, workbook, data, configs):
        for config in configs:
            sheet = workbook.add_worksheet(config.name[:31])
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, 'Account', bold)
            sheet.write(0, 1, 'Projected', bold)
            sheet.write(0, 2, 'Realized', bold)
            row = 1
            for account in config.account_ids:
                projections = self.env['account.projection'].search([
                    ('account_id', '=', account.id),
                    ('company_id', '=', config.company_id.id),
                ])
                projected_amount = sum(projections.mapped('amount'))
                realized_amount = sum(projections.mapped('amount_realized'))
                sheet.write(row, 0, account.display_name)
                sheet.write_number(row, 1, projected_amount)
                sheet.write_number(row, 2, realized_amount)
                row += 1
