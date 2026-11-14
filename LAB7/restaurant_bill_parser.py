def clean_dish_name(name):
    """
    Removes the chef's-special markers (*, #, ~) and title-cases the name.
    Hardened against None, non-strings, and unexpected symbols.
    """
    if name is None or not isinstance(name, str):
        return ""
    name = name.strip()
    for ch in ['*', '#', '~']:
        name = name.replace(ch, '')
    return name.strip().title()


def parse_item_prices(text):
    """
    Parses comma-separated prices into a list of ints.
    Hardened against None, empty items, non-integers, and malformed inputs.
    """
    if text is None or not isinstance(text, str):
        return []
    prices = []
    for item in text.split(','):
        item = item.strip()
        if not item:
            continue
        try:
            val = int(item)
            if val >= 0:
                prices.append(val)
        except ValueError:
            # Skip non-integer or malformed items gracefully
            continue
    return prices


def split_amount(text):
    """
    Splits 'TOTAL/PEOPLE' into the amount each person pays.
    Hardened against None, missing delimiters, non-numbers, negative values, and zero division.
    """
    if text is None or not isinstance(text, str):
        return 0
    parts = text.split('/')
    if len(parts) != 2:
        return 0
    try:
        total = int(parts[0].strip())
        people = int(parts[1].strip())
        if people <= 0 or total < 0:
            return 0
        return total // people
    except ValueError:
        return 0


def main():
    print("==== Running clean_dish_name ====")
    value = input("Enter a dish name from the menu (e.g. *paneer tikka*): ")
    print("Dish name:", clean_dish_name(value))

    print("\n==== Running parse_item_prices ====")
    value = input("Enter item prices separated by commas (e.g. 250,180,320): ")
    print("Item prices:", parse_item_prices(value))

    print("\n==== Running split_amount ====")
    value = input("Enter the bill and number of people as TOTAL/PEOPLE (e.g. 1200/4): ")
    print("Each person pays:", split_amount(value))


if __name__ == "__main__":
    main()
