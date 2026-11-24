from pricekit.cart import calculate_total


def test_member_bulk_discount():
    items = [{"price": 10, "qty": 10}]
    assert calculate_total(items, "member", None, None, False) == 80.0


def test_guest_no_discount():
    items = [{"price": 5, "qty": 2}]
    assert calculate_total(items, "guest", None, None, False) == 10.0


def test_coupon_save10():
    items = [{"price": 100, "qty": 1}]
    assert calculate_total(items, "guest", "SAVE10", None, False) == 90.0


def test_canada_tax():
    items = [{"price": 100, "qty": 1}]
    assert calculate_total(items, "guest", None, "CA", False) == 113.0