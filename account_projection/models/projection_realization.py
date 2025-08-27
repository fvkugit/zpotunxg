"""Partial realization of a projection."""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectionRealization(models.Model):
    """Links projections with real accounting documents."""

    _name = 'account.projection.realization'
    _description = 'Projection Realization'
    _rec_name = 'projection_id'

    projection_id = fields.Many2one(
        'account.projection', required=True, ondelete='cascade', index=True
    )
    move_id = fields.Many2one('account.move', required=True, index=True)
    company_id = fields.Many2one(related='projection_id.company_id', store=True)
    currency_id = fields.Many2one(
        'res.currency', related='projection_id.currency_id', store=True
    )
    amount = fields.Monetary(required=True)

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_('Amount must be positive.'))
