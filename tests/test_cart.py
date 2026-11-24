import pytest

from pricekit.cart import calculate_total, load_cart


def test_member_bulk_discount():
    assert calculate_total([{"price": 10, "qty": 10}], "member") == 80.0


def test_member_mid_and_low_tiers():
    assert calculate_total([{"price": 10, "qty": 5}], "member") == 45.0
    assert calculate_total([{"price": 10, "qty": 1}], "member") == 9.5


def test_guest_tiers():
    assert calculate_total([{"price": 5, "qty": 2}], "guest") == 10.0
    assert calculate_total([{"price": 10, "qty": 10}], "guest") == 95.0


def test_coupons():
    items = [{"price": 100, "qty": 1}]
    assert calculate_total(items, "guest", "SAVE10") == 90.0
    assert calculate_total(items, "guest", "SAVE20") == 80.0


def test_taxes():
    items = [{"price": 100, "qty": 1}]
    assert calculate_total(items, "guest", None, "CA") == 113.0
    assert calculate_total(items, "guest", None, "US") == 107.0


def test_invalid_items_ignored():
    items = [{"price": 10, "qty": 0}, {"price": -5, "qty": 2}]
    assert calculate_total(items, "guest") == 0.0


def test_unknown_customer_type_raises():
    with pytest.raises(ValueError):
        calculate_total([{"price": 10, "qty": 2}], "gold")


def test_load_cart_valid(tmp_path):
    f = tmp_path / "cart.json"
    f.write_text('[{"price": 1, "qty": 1}]', encoding="utf-8")
    assert load_cart(str(f)) == [{"price": 1, "qty": 1}]


def test_load_cart_missing_and_invalid(tmp_path):
    assert load_cart(str(tmp_path / "nope.json")) == []
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    assert load_cart(str(bad)) == []