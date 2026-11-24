import json

TIERS = {
    "member": ((10, 0.80), (5, 0.90), (0, 0.95)),
    "guest": ((10, 0.95), (0, 1.00)),
}
COUPONS = {"SAVE10": 0.90, "SAVE20": 0.80}
TAX_RATES = {"CA": 1.13, "US": 1.07}


def _line_total(item, tiers):
    qty, price = item["qty"], item["price"]
    if qty <= 0 or price <= 0:
        return 0.0
    for min_qty, factor in tiers:
        if qty >= min_qty:
            return price * qty * factor
    return 0.0


def calculate_total(items, customer_type, coupon=None, country=None):
    if customer_type not in TIERS:
        raise ValueError(f"Unknown customer type: {customer_type}")
    tiers = TIERS[customer_type]
    total = sum(_line_total(item, tiers) for item in items)
    total *= COUPONS.get(coupon, 1.0)
    total *= TAX_RATES.get(country, 1.0)
    return round(total, 2)


def load_cart(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []