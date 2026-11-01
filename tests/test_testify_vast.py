"""The credit sets how long a rented machine trains, and the machine stops itself."""

from buyscape.testify import vast


def test_the_credit_sets_the_hours_with_a_reserve_kept_back():
    assert vast.training_hours(11.13, 0.50) == round((11.13 - 1.0) / 0.50 - vast.SETUP_HOURS, 2)
    assert vast.training_hours(1.2, 0.50) == 0.0
    assert vast.training_hours(11.0, 0.5, reserve=3.0) == 15.5


def test_the_machine_runs_the_script_as_its_only_command_and_resumes_from_the_hub():
    script = vast.onstart("godzilla1215/testify-data", "godzilla1215/testify-2b-run6", "sft_r6.jsonl",
                          "--image-tokens 640", 18.5)
    assert "--resumable --hub-repo godzilla1215/testify-2b-run6 --hours 18.5 --image-tokens 640" in script
    assert script.index("hf download") < script.index("sft_lora.py") < script.index("hf upload") < script.index("DONE")
    body = vast.request_body(script, "token")
    assert body["runtype"] == "args" and body["args"][:2] == ["bash", "-c"] and "onstart" not in body
    assert body["env"] == {"HF_TRAIN_TOKEN": "token"}
