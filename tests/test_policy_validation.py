"""Policy validation tests for Robo-Drafter."""

from __future__ import annotations

import pytest
import yaml

from robo_drafter.policy import Policy


def test_default_policy_loads_and_preserves_valid_parameters():
    policy = Policy.from_yaml("config/default.yaml")

    assert policy.name == "default_policy"
    assert policy.version == 1
    assert policy.params["speed"] == 0.6
    assert policy.tasks["navigate"]["success_threshold"] == 0.7


@pytest.mark.parametrize(
    "document, message",
    [
        ("- not-a-mapping", "root must be a mapping"),
        ("name: ''\nversion: 1\nparams: {}\ntasks: {}", "name"),
        ("name: okay\nversion: 0\nparams: {}\ntasks: {}", "version"),
        ("name: okay\nversion: 1\nparams: []\ntasks: {}", "params"),
        ("name: okay\nversion: 1\nparams:\n  speed: 2.0\ntasks: {}", "between 0 and 1"),
        ("name: okay\nversion: 1\nparams:\n  retry_limit: -1\ntasks: {}", "retry_limit"),
        (
            "name: okay\nversion: 1\nparams: {}\ntasks:\n  pick:\n    goal: pick\n    success_threshold: 1.5",
            "success_threshold",
        ),
        (
            "name: okay\nversion: 1\nparams: {}\ntasks:\n  pick: []",
            "must be a mapping",
        ),
    ],
)
def test_invalid_policy_is_rejected(tmp_path, document, message):
    path = tmp_path / "bad.yaml"
    path.write_text(document, encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        Policy.from_yaml(path)


def test_policy_round_trip_is_stable(tmp_path):
    policy = Policy.from_yaml("config/default.yaml")
    destination = tmp_path / "policy" / "copy.yaml"
    policy.save(destination)
    restored = Policy.from_yaml(destination)

    assert restored.to_dict() == policy.to_dict()


def test_policy_clone_is_independent():
    policy = Policy.from_yaml("config/default.yaml")
    cloned = policy.clone()
    cloned.params["speed"] = 0.1

    assert policy.params["speed"] == 0.6
