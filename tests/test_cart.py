from pricekit.cart import calculate_total, load_cart


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

def test_load_cart_valid(tmp_path):
    f = tmp_path / "cart.json"
    f.write_text('[{"price": 1, "qty": 1}]', encoding="utf-8")
    assert load_cart(str(f)) == [{"price": 1, "qty": 1}]


def test_load_cart_missing_and_invalid(tmp_path):
    assert load_cart(str(tmp_path / "nope.json")) == []
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    assert load_cart(str(bad)) == []