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
