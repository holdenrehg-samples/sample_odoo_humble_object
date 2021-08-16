from odoo.models import Model
from odoo.tools import float_compare
from odoo.addons.stock.core import stock_availability


"""
This is just an example of refactoring a core Odoo methods using the humble
object pattern.

**DO NOT** include this code in your application because it would completley
override the _get_available_quantity method.

See the original method here:
https://github.com/odoo/odoo/blob/14.0/addons/stock/models/stock_quant.py#L307-L345
"""

class Quant(Model):
    def _get_available_quantity(
        self,
        product_id,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
        allow_negative=False,
    ):
        self = self.sudo()

        rounding = product_id.uom_id.rounding
        quants = self._gather(
            product_id,
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
        )

        available_quantities = stock_availability.availability_by_tracking(
            product_id.tracking, quants
        )

        if not allow_negative:
            available_quantities = filter(
                lambda qty: float_compare(qty, 0, precision_rounding=rounding) > 0,
                available_quantities,
            )

        return sum(available_quantities)
