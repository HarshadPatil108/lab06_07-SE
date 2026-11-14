import pytest
from restaurant_bill import bill_total, split_bill, table_wait

# ============================================================================
# Branch Coverage Test Suite for restaurant_bill.py
# Targets 100% Branch Coverage by testing every decision, condition, and edge case.
# ============================================================================

# --- Tests for bill_total branches ---

def test_bill_total_unknown_section():
    """Branch: section not in SERVICE_CHARGE (True branch)."""
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("invalid_section", 1000, 2, False)


def test_bill_total_negative_food_total():
    """Branch: food_total < 0 is True (compound condition branch 1)."""
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -50, 2, False)


def test_bill_total_zero_or_negative_guests():
    """Branch: food_total >= 0 is False, guests < 1 is True (compound condition branch 2)."""
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", 500, 0, False)


def test_bill_total_dine_in_regular():
    """Branch: is_happy_hour is False, guests < 8 (standard dine-in)."""
    # food_total: 1000, service: 100, total: 1100, tax 5%: 55 -> 1155
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_bill_total_dine_in_happy_hour():
    """Branch: is_happy_hour is True AND section != 'takeaway' (True branch)."""
    # food_total discounted by 20%: 800, service 10%: 80, total: 880, tax 5%: 44 -> 924
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_bill_total_takeaway_happy_hour():
    """Branch: is_happy_hour is True BUT section == 'takeaway' (False branch of section != 'takeaway')."""
    # No discount for takeaway. Service charge is 0%. total: 1000, tax 5%: 50 -> 1050
    assert bill_total("takeaway", 1000, 2, True) == 1050


def test_bill_total_rooftop_large_party_regular():
    """Branch: section == 'rooftop' (15% service charge), guests >= 8 (True branch for +200 service)."""
    # food_total: 2000, service: 300 + 200 = 500, total: 2500, tax 5%: 125 -> 2625
    assert bill_total("rooftop", 2000, 8, False) == 2625


def test_bill_total_rooftop_happy_hour_large_party():
    """Branch: rooftop with happy hour and guests >= 8."""
    # food_total: 2000 * 0.8 = 1600, service: 240 + 200 = 440, total: 2040, tax 5%: 102 -> 2142
    assert bill_total("rooftop", 2000, 10, True) == 2142


# --- Tests for split_bill branches ---

def test_split_bill_invalid_people():
    """Branch: people < 1 is True."""
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_split_bill_invalid_tip():
    """Branch: tip_percent < 0 is True."""
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 4, -5)


def test_split_bill_even_split():
    """Branch: grand_total % people == 0 (False branch for remainder check)."""
    # grand_total: 1000 + 10% = 1100, 1100 // 4 = 275 (exact)
    assert split_bill(1000, 4, 10) == 275


def test_split_bill_with_remainder():
    """Branch: grand_total % people != 0 (True branch for remainder check, share += 1)."""
    # grand_total: 100, 100 // 3 = 33, remainder 1 -> 34
    assert split_bill(100, 3, 0) == 34


# --- Tests for table_wait branches ---

def test_table_wait_oversized_party():
    """Branch: party_size > 12 is True -> 'call ahead'."""
    assert table_wait(13, 5, False) == "call ahead"


def test_table_wait_has_reservation():
    """Branch: party_size <= 12 is False, has_reservation is True -> 'seat now'."""
    assert table_wait(4, 0, True) == "seat now"


def test_table_wait_no_free_tables():
    """Branch: has_reservation is False, free_tables == 0 is True -> 'waitlist'."""
    assert table_wait(4, 0, False) == "waitlist"


def test_table_wait_large_party_limited_tables():
    """Branch: free_tables > 0, party_size > 6 (True) and free_tables < 2 (True) -> 'waitlist'."""
    assert table_wait(7, 1, False) == "waitlist"


def test_table_wait_small_party_one_table():
    """Branch: free_tables > 0, party_size <= 6 (False branch of party_size > 6) -> 'seat now'."""
    assert table_wait(5, 1, False) == "seat now"


def test_table_wait_large_party_multiple_tables():
    """Branch: free_tables > 0, party_size > 6 (True) but free_tables >= 2 (False branch of free_tables < 2) -> 'seat now'."""
    assert table_wait(8, 2, False) == "seat now"
