import math

from hypothesis import given, strategies as st
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers


# ---------- lookup_drink_code ----------

@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    try:
        result = lookup_drink_code(s)
    except Exception as e:
        assert False, f"lookup_drink_code crashed with: {type(e).__name__}: {e}"
    # result must be a known price or None (unknown / invalid code)
    assert result is None or isinstance(result, float)


@given(st.sampled_from(["LAT", "CAP", "ESP", "AME", "MOC"]), st.text())
def test_lookup_drink_code_valid_prefix(prefix, suffix):
    # any string starting with a valid code (any case) must give a price
    try:
        result = lookup_drink_code(prefix.lower() + suffix)
    except Exception as e:
        assert False, f"lookup_drink_code crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, float) and result > 0


# ---------- calculate_average_shot_cost ----------

@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    try:
        result = calculate_average_shot_cost(s)
    except Exception as e:
        assert False, f"calculate_average_shot_cost crashed with: {type(e).__name__}: {e}"
    # result must be None (invalid input) or a finite, non-negative number
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.lists(st.floats(min_value=0, max_value=1000, allow_nan=False), max_size=10))
def test_calculate_average_shot_cost_csv(prices):
    csv = ",".join(str(p) for p in prices)
    try:
        result = calculate_average_shot_cost(csv)
    except Exception as e:
        assert False, f"calculate_average_shot_cost crashed with: {type(e).__name__}: {e}"
    if prices:
        assert math.isclose(result, sum(prices) / len(prices), rel_tol=1e-9, abs_tol=1e-9)
    else:
        assert result is None  # empty list -> no divide-by-zero


# ---------- parse_order_modifiers ----------

@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    try:
        result = parse_order_modifiers(s)
    except Exception as e:
        assert False, f"parse_order_modifiers crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, dict)


@given(st.dictionaries(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=8),
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz:", max_size=8),
    max_size=5,
))
def test_parse_order_modifiers_roundtrip(mods):
    spec = ";".join(f"{k}:{v}" for k, v in mods.items())
    try:
        result = parse_order_modifiers(spec)
    except Exception as e:
        assert False, f"parse_order_modifiers crashed with: {type(e).__name__}: {e}"
    assert result == mods
