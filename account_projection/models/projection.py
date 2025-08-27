"""Financial projection models.

This module provides the base models to handle projected cashflow
entries. A projection represents an expected accounting movement that
may later be linked to real documents (account moves).
"""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Projection(models.Model):
    """Main projection model."""

    _name = 'account.projection'
    _description = 'Financial Projection'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, index=True, required=True
    )
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True
    )
    partner_id = fields.Many2one('res.partner', tracking=True, index=True)
    account_id = fields.Many2one(
        'account.account', tracking=True, index=True, required=True
    )
    category_id = fields.Many2one('account.projection.category', index=True)
    date_expected = fields.Date(required=True, index=True, tracking=True)
    amount = fields.Monetary(required=True, tracking=True)

    realization_ids = fields.One2many(
        'account.projection.realization', 'projection_id', string='Realizations'
    )
    amount_realized = fields.Monetary(
        compute='_compute_amounts', store=True, string='Amount Realized'
    )
    amount_remaining = fields.Monetary(
        compute='_compute_amounts', store=True, string='Remaining Amount'
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('projected', 'Projected'),
            ('partial', 'Partial'),
            ('realized', 'Realized'),
            ('cancelled', 'Cancelled'),
            ('dropped', 'Dropped'),
        ],
        default='draft',
        tracking=True,
    )

    @api.depends('amount', 'realization_ids.amount')
    def _compute_amounts(self):
        for rec in self:
            realized = sum(rec.realization_ids.mapped('amount'))
            rec.amount_realized = realized
            rec.amount_remaining = rec.amount - realized
            if rec.amount_remaining <= 0 and rec.amount > 0:
                rec.state = 'realized'
            elif realized:
                rec.state = 'partial'
            else:
                rec.state = 'projected'

    def action_mark_draft(self):
        self.write({'state': 'draft'})

    def action_mark_cancelled(self):
        self.write({'state': 'cancelled'})

    def action_mark_dropped(self):
        self.write({'state': 'dropped'})

    def action_link_move(self, move, amount):
        """Create a realization linking this projection with a move.

        :param move: account.move record to link.
        :param amount: Amount to link in the projection currency.
        """
        self.ensure_one()
        if amount <= 0:
            raise ValidationError(_('Linked amount must be positive.'))
        self.env['account.projection.realization'].create({
            'projection_id': self.id,
            'move_id': move.id,
            'amount': amount,
            'currency_id': self.currency_id.id,
            'company_id': self.company_id.id,
        })

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_('Amount must be positive.'))


class ProjectionCategory(models.Model):
    """Categorization helper for projections."""

    _name = 'account.projection.category'
    _description = 'Projection Category'
    _order = 'name'

    name = fields.Char(required=True)
    type = fields.Selection(
        [('in', 'Income'), ('out', 'Expense')], required=True, default='out'
    )
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
