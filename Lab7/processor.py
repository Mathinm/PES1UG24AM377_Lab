import math

MENU_PRICES = {
    "LAT": 4.50,
    "CAP": 4.00,
    "ESP": 3.00,
    "AME": 3.50,
    "MOC": 5.00,   # was "MOc" -> could never match after .upper()
}


def lookup_drink_code(code_string):
    """Return the base price for a drink code, or None if invalid/unknown."""
    if not isinstance(code_string, str):
        return None
    code_prefix = code_string.strip().upper()[:3]
    if len(code_prefix) < 3:
        return None
    return MENU_PRICES.get(code_prefix)   # .get() -> no KeyError


def calculate_average_shot_cost(pricing_csv):
    """Return the average of comma-separated shot prices, or None if invalid."""
    if not isinstance(pricing_csv, str):
        return None

    prices = []
    for part in pricing_csv.split(','):
        part = part.strip()
        if not part:                      # skip empty entries like "1.0,,2.0"
            continue
        try:
            value = float(part)
        except ValueError:                # "abc", "1.2.3" ...
            return None
        if not math.isfinite(value) or value < 0:   # nan, inf, negative price
            return None
        prices.append(value)

    if not prices:                        # avoid ZeroDivisionError
        return None

    average = math.fsum(prices) / len(prices)
    if not math.isfinite(average):        # overflow on huge values
        return None
    return average


def parse_order_modifiers(order_spec):
    """Parse 'key:value;key:value' into a dict. Malformed pairs are skipped."""
    modifier_dict = {}
    if not isinstance(order_spec, str):
        return modifier_dict

    for item in order_spec.split(';'):
        if ':' not in item:               # "milk" or "" -> skip
            continue
        key, value = item.split(':', 1)   # maxsplit=1 -> "a:b:c" is fine
        key = key.strip()
        if not key:                       # ":oat" -> skip
            continue
        modifier_dict[key] = value.strip()
    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    if price is None:
        print("Invalid or unknown drink code.")
    else:
        print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    if avg_price is None:
        print("Invalid shot price list.")
    else:
        print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
