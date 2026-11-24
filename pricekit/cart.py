import json


def calculate_total(items, customer_type, coupon, country, debug):
    total = 0.0
    tax_rate_unused = 0.13
    for item in items:
        if item["qty"] > 0:
            if item["price"] > 0:
                if customer_type == "member":
                    if item["qty"] >= 10:
                        total += item["price"] * item["qty"] * 0.80
                    elif item["qty"] >= 5:
                        total += item["price"] * item["qty"] * 0.90
                    else:
                        total += item["price"] * item["qty"] * 0.95
                elif customer_type == "guest":
                    if item["qty"] >= 10:
                        total += item["price"] * item["qty"] * 0.95
                    else:
                        total += item["price"] * item["qty"]
    if coupon == "SAVE10":
        total = total * 0.90
    elif coupon == "SAVE20":
        total = total * 0.80
    if country == "CA":
        total = total * 1.13
    elif country == "US":
        total = total * 1.07
    return round(total, 2)


def load_cart(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return []