"""The labeller: same checklist as the hand review, compared item by item."""

from pathlib import Path

from buyscape.testify.convert import load_items
from buyscape.testify.label import PhotoReview, agreement, request_for

ROOT = Path(__file__).resolve().parents[1]


def test_request_shows_the_labels_to_check_and_no_contact_details(tmp_path):
    item = next(i for i in load_items(ROOT / "eval" / "testify" / "items.jsonl") if i.source == "jiji" and i.seller_text)
    item.seller_text = "Call 08012345678 now"
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"x")
    req = request_for(item, [photo, photo, photo, photo])
    assert "0801" not in req.user_text and "[phone]" in req.user_text
    assert item.answer.title in req.user_text and "tier=" in req.user_text
    assert len(req.images) == 3 and req.output_schema is PhotoReview


def test_agreement_counts_only_shared_items():
    ai = {"a": {"keep_in_benchmark": "keep", "photo_issues": ["none"]},
          "b": {"keep_in_benchmark": "drop", "photo_issues": ["stock_or_catalogue_photo"]},
          "z": {"keep_in_benchmark": "drop"}}
    ref = {"a": {"keep_in_benchmark": "keep", "photo_issues": []},
           "b": {"keep_in_benchmark": "keep", "photo_issues": ["stock_or_catalogue_photo"]}}
    out = agreement(ai, ref)
    assert out["keep_in_benchmark"] == {"items": 2, "agree": 1, "rate": 0.5}
    assert out["stock_photo_flag"]["rate"] == 1.0


def test_photos_are_found_inside_the_item_cache_folder(tmp_path):
    from buyscape.testify.label import photos_for

    item = next(i for i in load_items(ROOT / "eval" / "testify" / "items.jsonl") if i.source == "jiji" and i.photos.cache)
    folder = tmp_path / item.photos.cache
    folder.mkdir(parents=True)
    for name in ("01.webp", "00.webp"):
        (folder / name).write_bytes(b"x")
    assert [p.name for p in photos_for(item, tmp_path)] == ["00.webp", "01.webp"]


def test_the_rule_decides_not_the_reviewers_vote():
    from buyscape.testify.rules import drop_reason

    assert drop_reason({"looks_actually_used": "no", "keep_in_benchmark": "keep"}) == "new stock, not second-hand"
    assert drop_reason({"looks_actually_used": "yes", "photo_issues": ["stock_or_catalogue_photo"]})
    assert drop_reason({"looks_actually_used": "yes", "tier": "not_for_sale"})
    assert drop_reason({"looks_actually_used": "yes", "keep_in_benchmark": "drop", "drop_reason": "lot"}) == "lot"
    assert drop_reason({"looks_actually_used": "yes", "photo_issues": ["watermark_or_logo"], "keep_in_benchmark": "keep"}) is None
