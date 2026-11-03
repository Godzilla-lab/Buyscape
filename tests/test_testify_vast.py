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
    body = vast.request_body(script)
    assert body["runtype"] == "args" and body["args"][:2] == ["bash", "-c"] and "onstart" not in body
    assert body["env"] == {}, "the token comes from the Vast account, never from here"
    assert vast.request_body(script, "token")["env"] == {"HF_TRAIN_TOKEN": "token"}


def test_no_script_echoes_the_token_into_a_log():
    for script in (vast.onstart("d", "r", "f.jsonl", "", 2.0), vast.read_onstart("d", "r", "job1", 40)):
        assert "--token" not in script
        assert script.index('export HF_TOKEN="$HF_TRAIN_TOKEN"') < script.index("set -x")


def test_a_reading_machine_serves_the_model_reads_in_parts_and_always_sends_back_what_it_has():
    script = vast.read_onstart("godzilla1215/d", "godzilla1215/r", "test100", 40, parallel=8)
    assert script.startswith('test -n "$HF_TRAIN_TOKEN"') and "timeout 40m bash -c" in script
    assert "vllm serve Qwen/Qwen3-VL-32B-Instruct-FP8" in script and "--max-num-seqs 16" in script
    assert "split -n l/8 -d ids.txt part_" in script and "--model vllm:Qwen/Qwen3-VL-32B-Instruct-FP8" in script
    assert "--reads-only" in script and "--tag test100_$p" in script
    assert "curl" not in script, "the image has no curl"
    assert "wait $pids" in script and "; wait\n" not in script, "a bare wait also waits for the model server"
    assert "mkdir -p job/docs/proof" in script and "while sleep 1800" in script
    # The upload is outside the time limit, so a run cut short still sends back its reads and logs.
    assert script.index("timeout 40m") < script.index("EXIT") < script.rindex("hf upload godzilla1215/r /workspace/out reads/test100")


def test_a_bundle_holds_the_code_the_pool_and_only_the_wanted_photos(tmp_path, monkeypatch):
    import json
    import subprocess
    import tarfile

    for rel in ("src/buyscape/x.py", "protocols/p.yaml"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text("x")
    pool = tmp_path / "eval" / "testify" / "train_pool.jsonl"
    pool.parent.mkdir(parents=True)
    rows = []
    for i in ("a1", "b2"):
        media = tmp_path / "eval" / "raw" / "testify_crawl" / "media" / i
        media.mkdir(parents=True)
        (media / "00.jpg").write_bytes(b"jpg")
        rows.append({"id": i, "source": "jiji", "url": f"https://jiji.ng/{i}", "split": "train", "tier": "small_goods",
                     "market": "lagos", "currency": "NGN",
                     "photos": {"count": 1, "public": False, "cache": f"eval/raw/testify_crawl/media/{i}/"},
                     "answer": {"title": "LG fridge", "kind": None, "identity": {"text": "fridge"},
                                "price": {"ngn": 90000, "kind": "asking", "source": "jiji"}}})
    pool.write_text("".join(json.dumps(r) + "\n" for r in rows))
    monkeypatch.setattr(vast.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
        a, 0, stdout="src/buyscape/x.py\nprotocols/p.yaml\n"))
    counts = vast.bundle(tmp_path, ["a1", "zz"], tmp_path / "out")
    assert counts["adverts"] == 1 and counts["not in the pool"] == 1 and counts["photos"] == 1
    with tarfile.open(tmp_path / "out" / "photos.tar") as tar:
        assert tar.getnames() == ["eval/raw/testify_crawl/media/a1/00.jpg"]
    with tarfile.open(tmp_path / "out" / "code.tar.gz") as tar:
        assert {"src/buyscape/x.py", "protocols/p.yaml", "eval/testify/train_pool.jsonl"} <= set(tar.getnames())
    assert (tmp_path / "out" / "ids.txt").read_text() == "a1\n"


def test_a_model_served_on_the_rented_machine_is_called_there(monkeypatch):
    from buyscape.providers.openrouter import OpenRouterProvider

    monkeypatch.setenv("VLLM_API_KEY", "local")
    monkeypatch.delenv("VLLM_URL", raising=False)
    assert OpenRouterProvider("Qwen/Qwen3-VL-32B-Instruct-FP8", vendor="vllm")._url == \
        "http://127.0.0.1:8000/v1/chat/completions"


def test_a_training_machine_downloads_only_its_own_folder():
    script = vast.onstart("godzilla1215/d", "godzilla1215/r", "sft_r6.jsonl", "--epochs 1", 5.0, folder="train6")
    assert "--include train6/* 'train6/**'" in script or "--include 'train6/*' 'train6/**'" in script
    assert "python data/train6/sft_lora.py" in script and "--data data/train6/sft_r6.jsonl --root data/train6" in script
