from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import app.challenge as challenge_config
from app.challenge import load_challenge


class ChallengeConfigTests(unittest.TestCase):
    def test_missing_challenge_explains_that_coach_has_not_released_it(self) -> None:
        missing_path = Path(tempfile.gettempdir()) / "day13-missing-challenge.json"
        if missing_path.exists():
            missing_path.unlink()

        with self.assertRaisesRegex(FileNotFoundError, "chưa được Lab Coach release"):
            load_challenge(missing_path)

    def test_valid_challenge_is_loaded(self) -> None:
        payload = {
            "cohort": "K3",
            "challenge_id": "day13-k3",
            "incident": "rag_slow",
            "seed": 1303,
            "affected_feature": "refund",
            "latency_threshold_ms": 2000,
            "queries": [
                {
                    "user_id": "k3-01",
                    "session_id": "challenge-k3",
                    "feature": "refund",
                    "message": "What evidence explains the latency increase?",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            challenge_path = Path(temp_dir) / "challenge.json"
            challenge_path.write_text(json.dumps(payload), encoding="utf-8")
            challenge = load_challenge(challenge_path)

        self.assertEqual(challenge.cohort, "K3")
        self.assertEqual(challenge.incident, "rag_slow")
        self.assertEqual(challenge.queries[0]["feature"], "refund")

    def test_unknown_incident_is_rejected(self) -> None:
        payload = {
            "cohort": "K4",
            "challenge_id": "day13-k4",
            "incident": "answer_leak",
            "seed": 1304,
            "affected_feature": "monitoring",
            "latency_threshold_ms": 2000,
            "queries": [
                {
                    "user_id": "k4-01",
                    "session_id": "challenge-k4",
                    "feature": "monitoring",
                    "message": "Find the affected span.",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            challenge_path = Path(temp_dir) / "challenge.json"
            challenge_path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incident không hợp lệ"):
                load_challenge(challenge_path)

    def test_explicit_practice_incident_does_not_require_release_file(self) -> None:
        missing_path = Path(tempfile.gettempdir()) / "day13-no-release-needed.json"

        incident = challenge_config.resolve_incident("tool_fail", missing_path)

        self.assertEqual(incident, "tool_fail")

    def test_official_incident_comes_from_release_file(self) -> None:
        payload = {
            "cohort": "K4",
            "challenge_id": "day13-k4",
            "incident": "rag_slow",
            "seed": 1304,
            "affected_feature": "monitoring",
            "latency_threshold_ms": 2000,
            "queries": [
                {
                    "user_id": "k4-01",
                    "session_id": "challenge-k4",
                    "feature": "monitoring",
                    "message": "Find the affected span.",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            challenge_path = Path(temp_dir) / "challenge.json"
            challenge_path.write_text(json.dumps(payload), encoding="utf-8")
            incident = challenge_config.resolve_incident(None, challenge_path)

        self.assertEqual(incident, "rag_slow")

    def test_query_order_is_deterministic_for_the_released_seed(self) -> None:
        challenge = challenge_config.ChallengeConfig(
            cohort="K3",
            challenge_id="day13-k3",
            incident="rag_slow",
            seed=1303,
            affected_feature="refund",
            latency_threshold_ms=2000,
            queries=tuple(
                {
                    "user_id": user_id,
                    "session_id": "challenge-k3",
                    "feature": "refund",
                    "message": f"Question {user_id}",
                }
                for user_id in ("u1", "u2", "u3")
            ),
        )

        ordered = challenge_config.ordered_queries(challenge)

        self.assertEqual([query["user_id"] for query in ordered], ["u1", "u3", "u2"])


if __name__ == "__main__":
    unittest.main()
