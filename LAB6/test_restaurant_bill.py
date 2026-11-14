import pytest
from restaurant_bill import bill_total, split_bill, table_wait

# ============================================================================
# Test Suite for restaurant_bill.py (Lab 6)
# ============================================================================

# --- Tests for bill_total ---

def test_dine_in_bill():
    """Initial test case: Standard dine-in calculation."""
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_bill_total_unknown_section():
    """Branch: section not in SERVICE_CHARGE (True branch)."""
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("invalid_section", 1000, 2, False)


def test_bill_total_negative_food_total():
    """Branch: food_total < 0 is True."""
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -50, 2, False)


def test_bill_total_zero_or_negative_guests():
    """Branch: food_total >= 0, guests < 1 is True."""
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", 500, 0, False)


def test_bill_total_dine_in_happy_hour():
    """Branch: is_happy_hour is True AND section != 'takeaway'."""
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_bill_total_takeaway_happy_hour():
    """Branch: is_happy_hour is True BUT section == 'takeaway'."""
    assert bill_total("takeaway", 1000, 2, True) == 1050


def test_bill_total_rooftop_large_party_regular():
    """Branch: section == 'rooftop' (15% service charge), guests >= 8."""
    assert bill_total("rooftop", 2000, 8, False) == 2625


def test_bill_total_rooftop_happy_hour_large_party():
    """Branch: rooftop with happy hour and guests >= 8."""
    assert bill_total("rooftop", 2000, 10, True) == 2142


# --- Tests for split_bill ---

def test_even_split():
    """Initial test case: Even split with tip."""
    assert split_bill(1000, 4, 10) == 275


def test_split_bill_invalid_people():
    """Branch: people < 1 is True."""
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_split_bill_invalid_tip():
    """Branch: tip_percent < 0 is True."""
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 4, -5)


def test_split_bill_with_remainder():
    """Branch: grand_total % people != 0 (remainder check, share += 1)."""
    assert split_bill(100, 3, 0) == 34


# --- Tests for table_wait ---

def test_table_wait_oversized_party():
    """Branch: party_size > 12 is True -> 'call ahead'."""
    assert table_wait(13, 5, False) == "call ahead"


def test_table_wait_has_reservation():
    """Branch: party_size <= 12, has_reservation is True -> 'seat now'."""
    assert table_wait(4, 0, True) == "seat now"


def test_table_wait_no_free_tables():
    """Branch: has_reservation is False, free_tables == 0 is True -> 'waitlist'."""
    assert table_wait(4, 0, False) == "waitlist"


def test_table_wait_large_party_limited_tables():
    """Branch: free_tables > 0, party_size > 6 and free_tables < 2 -> 'waitlist'."""
    assert table_wait(7, 1, False) == "waitlist"


def test_table_wait_small_party_one_table():
    """Branch: free_tables > 0, party_size <= 6 -> 'seat now'."""
    assert table_wait(5, 1, False) == "seat now"


def test_table_wait_large_party_multiple_tables():
    """Branch: free_tables > 0, party_size > 6 but free_tables >= 2 -> 'seat now'."""
    assert table_wait(8, 2, False) == "seat now"
