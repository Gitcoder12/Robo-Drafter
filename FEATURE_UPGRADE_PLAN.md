# Robo-Drafter — Feature Upgrade Plan

**Snapshot:** 2026-11-13

## Product/research objective

A research prototype that experiments with changing robot configuration or policy settings based on how well a simulated task performs.

## P0 — correctness, scope and evidence

- [ ] Define a stable task/environment interface and deterministic evaluator contract.
- [ ] Compare mutation strategies to a fixed baseline over repeatable seeds and report variance.

## P1 — complete workflow

- [ ] Add experiment manifests, saved configurations, fitness histories and reproducible reruns.
- [ ] Add safety bounds and reject malformed or physically impossible configurations in simulation.

## P2 — differentiation and scale

- [ ] Add optional adapters for a supported simulator after defining the interface.
- [ ] Evaluate generalisation across tasks and configurations before making robotics-performance claims.

## Contribution-sized work packages

1. Reproduce one defect or establish one measurable research question.
2. Implement one bounded fix or experiment with focused tests.
3. Publish commands, environment, inputs, outputs and failure modes.
4. Add a reviewer-readable explanation and update ACTIVITY_LOG.md.

## Definition of done

- [ ] Clean setup succeeds from documented instructions.
- [ ] Tests/evaluations include happy path, boundary cases and failures.
- [ ] Results are reproducible and claims match the measured evidence.
- [ ] A human reviewer can inspect the diff and approve the scope.
