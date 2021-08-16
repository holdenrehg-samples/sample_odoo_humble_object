import unittest
from dataclasses import dataclass
from functools import reduce
from .. import stock_availability as stock


@dataclass
class QuantMock:
    quantity: float
    reserved_quantity: float
    lot_id: int = None


class TestStock(unittest.TestCase):
    def test_qty_available(self):
        quant = QuantMock(quantity=12.5, reserved_quantity=5.2)
        assert stock.qty_available(quant) == 7.3

    def test_sum_availability(self):
        quants = [
            QuantMock(quantity=11.0, reserved_quantity=2.0),
            QuantMock(quantity=11.0, reserved_quantity=3.0),
            QuantMock(quantity=11.0, reserved_quantity=4.0),
        ]
        assert reduce(stock.sum_availability, quants, 0) == 24.0

    def test_filter_tracked_quants(self):
        quants = [
            QuantMock(quantity=11.0, reserved_quantity=2.0, lot_id=2),
            QuantMock(quantity=11.0, reserved_quantity=2.0, lot_id=7),
            QuantMock(quantity=11.0, reserved_quantity=3.0, lot_id=None),
        ]

        filtered = list(filter(stock.filter_tracked, quants))
        assert len(filtered) == 2
        assert filtered == [quants[0], quants[1]]

    def test_filter_untracked_quants(self):
        quants = [
            QuantMock(quantity=11.0, reserved_quantity=2.0, lot_id=2),
            QuantMock(quantity=11.0, reserved_quantity=2.0, lot_id=7),
            QuantMock(quantity=11.0, reserved_quantity=3.0, lot_id=None),
        ]

        filtered = list(filter(stock.filter_untracked, quants))
        assert len(filtered) == 1
        assert filtered == [quants[2]]

    def test_availability_by_tracking_without_lots(self):
        quants = [
            QuantMock(quantity=11.0, reserved_quantity=2.0),
            QuantMock(quantity=11.0, reserved_quantity=3.0),
            QuantMock(quantity=11.0, reserved_quantity=4.0),
        ]

        assert stock.availability_by_tracking("none", quants) == [24.0]

    def test_availability_by_tracking_with_lots(self):
        quants = [
            QuantMock(quantity=11.0, reserved_quantity=2.0),
            QuantMock(quantity=11.0, reserved_quantity=3.0, lot_id=1),
            QuantMock(quantity=11.0, reserved_quantity=4.0, lot_id=2),
            QuantMock(quantity=11.0, reserved_quantity=5.0, lot_id=3),
            QuantMock(quantity=11.0, reserved_quantity=5.0, lot_id=3),
        ]

        quantities = stock.availability_by_tracking("lots", quants)
        assert quantities == [
            9.0,  # untracked
            8.0,  # lot_id=1
            7.0,  # lot_id=2
            12.0,  # lot_id=3
        ]
