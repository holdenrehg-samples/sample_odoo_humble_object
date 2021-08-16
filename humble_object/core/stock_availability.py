from typing import List, Dict
from functools import reduce


def qty_available(quant) -> float:
    """Rule for the definition of "available quantity" based on 1 quant object."""
    return quant.quantity - quant.reserved_quantity


def sum_availability(val, quant) -> float:
    """Reducer function to sum a collection of quants."""
    return val + qty_available(quant)


def filter_tracked(quant) -> bool:
    """Filter function that flags tracked quants to be filtered."""
    return quant.lot_id is not None


def filter_untracked(quant) -> bool:
    """Filter function that flags untracked quants to be filtered."""
    return quant.lot_id is None


def availability_by_tracking(tracking, quants) -> List[float]:
    """
    Returns a list of available quantities based on a tracking status. Without
    tracking all of the quantities are summed together. With tracking the
    quantities are summed per lot.

    This does not provide mapping between the quantities and the lot numbers.
    Use the quantities_per_lot() function for that.

        availability_by_tracking("none", (stock.quant(1), stock.quant(2)))
            [56.0]

        availability_by_tracking("lot", (stock.quant(1), stock.quant(2), stock.quant(3)))
            [45.2, 34.9]
    """
    if tracking == "none":
        return [reduce(sum_availability, quants, 0)]
    return list(quantities_per_lot(quants).values())


def quantities_per_lot(quants) -> Dict[str, float]:
    """
    Generates a quantity per lot map. Example return value looks like:

        {
            "untracked": 12.5,
            "lot_1": 10.0,
            "lot_2": 11.0,
            "lot_3": 12.0,

            ...
        }
    """

    tracked_quants = list(filter(filter_tracked, quants))
    untracked_quants = list(filter(filter_untracked, quants))

    res = {
        "untracked": reduce(sum_availability, untracked_quants, 0),
    }
    for quant in tracked_quants:
        res[quant.lot_id] = res.get(quant.lot_id, 0.0) + qty_available(quant)
    return res
