"""Extensions to account.move for projection suggestions."""

from odoo import api, fields, models, _
from odoo.osv import expression


class AccountMove(models.Model):
    _inherit = 'account.move'

    projection_match_ids = fields.Many2many(
        'account.projection', compute='_compute_projection_matches'
    )

    @api.depends('partner_id', 'line_ids.account_id', 'date', 'invoice_date')
    def _compute_projection_matches(self):
        Projection = self.env['account.projection']
        for move in self:
            domain = [
                ('state', 'in', ['projected', 'partial']),
                ('company_id', '=', move.company_id.id),
            ]
            subdomains = []
            if move.partner_id:
                subdomains.append([('partner_id', '=', move.partner_id.id)])
            account_ids = move.line_ids.mapped('account_id').ids
            if account_ids:
                subdomains.append([('account_id', 'in', account_ids)])
            if subdomains:
                domain = expression.AND([domain, expression.OR(subdomains)])
            date = move.invoice_date or move.date
            if date:
                domain.append(('date_expected', '=', date))
            move.projection_match_ids = Projection.search(domain)

    @api.onchange('partner_id', 'line_ids', 'date', 'invoice_date')
    def _onchange_projection_warning(self):
        self._compute_projection_matches()
        if self.projection_match_ids:
            return {
                'warning': {
                    'title': _('Related projections found'),
                    'message': _(
                        'There are projections that may relate to this document. '
                        'Use the Link Projection button to associate.'
                    ),
                }
            }

    def action_open_projection_wizard(self):
        self.ensure_one()
        ctx = {
            'default_move_id': self.id,
            'projection_ids': self.projection_match_ids.ids,
        }
        return {
            'name': _('Link Projection'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.projection.link.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
        }
