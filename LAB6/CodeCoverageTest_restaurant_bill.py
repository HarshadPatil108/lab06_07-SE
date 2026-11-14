import pytest
from restaurant_bill import bill_total, split_bill, table_wait

# Initial test cases from lab handout
def test_dine_in_bill():
    assert bill_total("dine_in", 1000, 2, False) == 1155

def test_even_split():
    assert split_bill(1000, 4, 10) == 275

# Additional test cases to achieve 100% line (code) coverage:

def test_bill_total_unknown_section():
    # Covers line 5-6 (raises ValueError for unknown section)
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("outdoor", 1000, 2, False)

def test_bill_total_invalid_order():
    # Covers line 7-8 (raises ValueError for food_total < 0)
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -100, 2, False)

def test_bill_total_happy_hour():
    # Covers line 9-10 (happy hour 20% discount applied)
    # food_total: 1000 -> 800, service 10%: 80, total: 880, tax 5%: 44 -> 924
    assert bill_total("dine_in", 1000, 2, True) == 924

def test_bill_total_large_party_service():
    # Covers line 12-13 (guests >= 8 adds 200 service charge)
    # food_total: 1000, service: 100 + 200 = 300, total: 1300, tax 5%: 65 -> 1365
    assert bill_total("dine_in", 1000, 8, False) == 1365

def test_split_bill_invalid_people():
    # Covers line 19-20 (raises ValueError for people < 1)
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)

def test_split_bill_invalid_tip():
    # Covers line 21-22 (raises ValueError for tip_percent < 0)
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 4, -5)

def test_split_bill_with_remainder():
    # Covers line 25-26 (grand_total % people != 0 increments share)
    # total: 100, tip 0% -> 100, share: 100 // 3 = 33 + 1 = 34
    assert split_bill(100, 3, 0) == 34

def test_table_wait_call_ahead():
    # Covers line 31-32 (party_size > 12)
    assert table_wait(13, 2, False) == "call ahead"

def test_table_wait_has_reservation():
    # Covers line 33-34 (has_reservation is True)
    assert table_wait(4, 0, True) == "seat now"

def test_table_wait_no_free_tables():
    # Covers line 35-36 (free_tables == 0)
    assert table_wait(4, 0, False) == "waitlist"

def test_table_wait_large_party_limited_tables():
    # Covers line 37-38 (party_size > 6 and free_tables < 2)
    assert table_wait(8, 1, False) == "waitlist"

def test_table_wait_seat_now():
    # Covers line 39 (normal walk-in with available tables)
    assert table_wait(4, 2, False) == "seat now"
