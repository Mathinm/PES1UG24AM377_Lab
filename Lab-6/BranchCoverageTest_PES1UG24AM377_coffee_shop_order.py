"""Lab 6 - Branch coverage tests for coffee_shop_order.py
SRN: PES1UG24AM377

Goal: drive every decision (if/elif/else, loops, break/continue)
both True and False (>= 90% branch coverage).
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


# ---- extra branch cases ----

def test_negative_tax_rate_raises():
    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


def test_empty_order_list_is_no_sale():
    assert process_order_batch([], 0.1) == {"total": 0.0, "status": "NO_SALE"}


def test_defaults_missing_paid_and_size():
    # no "paid" key -> skipped; paid w/o "size" -> medium default
    orders = [{"size": "large"}, {"paid": True}]
    assert process_order_batch(orders, 0.0) == {"total": 4.5, "status": "COMPLETED"}


def test_non_strict_allergen_alert_keeps_processing():
    # allergen_alert False-branch of strict_allergy: loop continues
    orders = [{
        "paid": True, "size": "medium", "strict_allergy": False,
        "customizations": [
            {"type": "allergen_alert", "cost": 0.0},
            {"type": "standard", "cost": 0.5},
        ],
    }]
    assert process_order_batch(orders, 0.0) == {"total": 5.0, "status": "COMPLETED"}


def test_syrup_cost_capped_at_1_5():
    orders = [{"paid": True, "size": "small",
               "customizations": [{"type": "syrup", "cost": 3.0}]}]
    assert process_order_batch(orders, 0.0) == {"total": 4.5, "status": "COMPLETED"}


def test_syrup_exactly_1_5_not_capped():
    orders = [{"paid": True, "size": "small",
               "customizations": [{"type": "syrup", "cost": 1.5}]}]
    assert process_order_batch(orders, 0.0) == {"total": 4.5, "status": "COMPLETED"}


def test_mod_with_missing_type_and_cost():
    orders = [{"paid": True, "size": "small", "customizations": [{}]}]
    assert process_order_batch(orders, 0.0) == {"total": 3.0, "status": "COMPLETED"}


def test_exactly_four_rejections_not_audited():
    orders = [{"paid": True, "size": "bad"} for _ in range(4)]
    orders.append({"paid": True, "size": "small"})
    assert process_order_batch(orders, 0.0) == {"total": 3.0, "status": "COMPLETED"}


def test_audit_rejected_takes_priority_over_no_sale():
    orders = [{"paid": True, "size": "bad"} for _ in range(5)]
    assert process_order_batch(orders, 0.1) == {"total": 0.0, "status": "AUDIT_REJECTED"}


# ---------------- check_espresso_machine ----------------

def test_espresso_no_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_espresso_shutdown_on_two_consecutive_overheats():
    assert check_espresso_machine([[97.0, 98.0]]) == "SHUTDOWN"


def test_espresso_optimal_with_streak_reset():
    assert check_espresso_machine([[97.0, 90.0, 97.0]]) == "OPTIMAL"


def test_espresso_none_is_no_data():
    assert check_espresso_machine(None) == "NO_DATA"


def test_espresso_streak_resets_between_cycles():
    # one overheat at end of cycle 1 + one at start of cycle 2 != shutdown
    assert check_espresso_machine([[90.0, 97.0], [97.0, 90.0]]) == "OPTIMAL"


def test_espresso_exactly_96_is_not_overheat():
    assert check_espresso_machine([[96.0, 96.0, 96.0]]) == "OPTIMAL"


def test_espresso_empty_inner_cycle_then_shutdown():
    assert check_espresso_machine([[], [99.0, 99.5]]) == "SHUTDOWN"
