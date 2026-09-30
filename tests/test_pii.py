from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_vietnamese_phone_formats() -> None:
    phone_numbers = (
        "0901234567",
        "090 123 4567",
        "090.123.4567",
        "090-123-4567",
        "+84 90 123 4567",
    )

    for phone_number in phone_numbers:
        out = scrub_text(f"Contact: {phone_number}")
        assert phone_number not in out
        assert "REDACTED_PHONE_VN" in out


def test_scrub_cccd() -> None:
    out = scrub_text("CCCD của tôi là 012345678901")
    assert "012345678901" not in out
    assert "REDACTED_CCCD" in out


def test_scrub_common_credit_card_formats() -> None:
    card_numbers = (
        "4111111111111111",
        "4111 1111 1111 1111",
        "4111-1111-1111-1111",
    )

    for card_number in card_numbers:
        out = scrub_text(f"Card: {card_number}")
        assert card_number not in out
        assert "REDACTED_CREDIT_CARD" in out


def test_scrub_passport() -> None:
    out = scrub_text("Hộ chiếu B1234567")
    assert "B1234567" not in out
    assert "REDACTED_PASSPORT" in out

def test_scrub_address() -> None:
    out = scrub_text("địa chỉ 12 đường Láng, phường Láng Thượng, quận Đống Đa, Hà Nội")
    assert "đường Láng, phường Láng Thượng, quận Đống Đa, Hà Nội" not in out
    assert "REDACTED_ADDRESS" in out