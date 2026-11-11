"""Lab 6 - Code (line) coverage tests for coffee_shop_order.py
SRN: PES1UG24AM377

Goal: execute every statement at least once (>= 90% line coverage).
"""
import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# ---------------- process_order_batch ----------------

def test_single_medium_coffee():
    orders = [{"paid": True, "size": "medium",
               "customizations": [{"type": "standard", "cost": 0.5}]}]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 5.5, "status": "COMPLETED"}


def test_invalid_input_raises():
    with pytest.raises(ValueError):
        process_order_batch("not a list", 0.1)


def test_unpaid_order_skipped_gives_no_sale():
    result = process_order_batch([{"paid": False, "size": "large"}], 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_small_large_and_unknown_size():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "large"},
        {"paid": True, "size": "venti"},   # rejected
    ]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 9.0, "status": "COMPLETED"}


def test_negative_cost_syrup_and_member_discount():
    orders = [{
        "paid": True, "size": "small", "is_member": True,
        "customizations": [
            {"type": "standard", "cost": -1.0},   # rejected
            {"type": "syrup", "cost": 1.0},
        ],
    }]
    # (3.0 + 1.0) * 0.9 = 3.6
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.6, "status": "COMPLETED"}


def test_strict_allergy_zeroes_item():
    orders = [{
        "paid": True, "size": "large", "strict_allergy": True,
        "customizations": [{"type": "allergen_alert", "cost": 0.0}],
    }]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_audit_rejected_when_more_than_four_rejections():
    orders = [{"paid": True, "size": "bad"} for _ in range(5)]
    orders.append({"paid": True, "size": "medium"})
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 4.5, "status": "AUDIT_REJECTED"}


# ---------------- check_espresso_machine ----------------

def test_espresso_no_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_espresso_shutdown_on_two_consecutive_overheats():
    assert check_espresso_machine([[97.0, 98.0]]) == "SHUTDOWN"


def test_espresso_optimal_with_streak_reset():
    assert check_espresso_machine([[97.0, 90.0, 97.0]]) == "OPTIMAL"
