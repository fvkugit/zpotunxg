"""Wizard to link account moves with projections."""

from odoo import api, fields, models, _


class ProjectionLinkWizard(models.TransientModel):
    """Allow the user to link an account move with an existing projection."""

    _name = 'account.projection.link.wizard'
    _description = 'Link Move to Projection'

    move_id = fields.Many2one('account.move', required=True, readonly=True)
    projection_id = fields.Many2one(
        'account.projection',
        required=True,
        domain="[('id', 'in', context.get('projection_ids', []))]",
    )
    currency_id = fields.Many2one(related='move_id.company_currency_id', readonly=True)
    amount = fields.Monetary(required=True, currency_field='currency_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('projection_ids'):
            res.setdefault('projection_id', self.env.context['projection_ids'][0])
        return res

    def action_link(self):
        self.ensure_one()
        self.projection_id.action_link_move(self.move_id, self.amount)
        return {'type': 'ir.actions.act_window_close'}
