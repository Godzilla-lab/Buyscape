"""A seller is read off the advert: the name in Jiji's photo stamp, read
through a faint watermark, and the phone number in the seller's words."""

from buyscape.testify.sellers import keys, phones, same, stamp_name


def _box(text, height=10):
    return (text, 0.9, [[0, 0], [1, 0], [1, height], [0, height]])


def test_the_name_beside_a_partly_read_stamp_is_the_seller():
    assert stamp_name([_box("POSTED ONJIH"), _box("YOOLAIFEOLUWA", 30), _box("PSR-550")]) == "YOOLAIFEOLUWA"
    assert stamp_name([_box("MCSTEVE", 30), _box("POSTED ON JIJI")]) == "MCSTEVE"
    assert stamp_name([_box("Nikon"), _box("D750")]) is None


def test_a_name_read_through_the_watermark_still_matches_and_different_sellers_do_not():
    assert same("name:QLAJIDEAMOSBISHOP", "name:OLAJIDEAMOSBISHOP")
    assert not same("name:MCSTEVE", "name:SMATECH")
    assert same("phone:8031234567", "phone:8031234567") and not same("phone:8031234567", "name:MCSTEVE")


def test_phone_numbers_in_any_spelling_are_one_key():
    assert phones("call 0803 123 4567 or +2348031234567") == {"8031234567"}
    assert keys([[_box("POSTED ON JIJI"), _box("MCSTEVE", 30)]], "call 08031234567") == {
        "name:MCSTEVE", "phone:8031234567"}
