"""Regression test from docs/trace_case.md: seeded_regression C-014@11 (FM-05 -> FM-08).

The agent subtracts the prior refund itself (step 5 `proposal` 120000) before calling the host,
the host subtracts it again, so the ledger holds 90000 while the reply still says 120.000đ.
Must FAIL on seeded_regression and PASS on fixed.
"""
import pytest

pytestmark = pytest.mark.student


def _ctx(case):
    from pydantic_evals.evaluators import EvaluatorContext

    return EvaluatorContext(name="C-014@11", inputs={}, metadata=None, expected_output=case["label"],
                            output=case["trial"], duration=0.0, _span_tree=None, attributes={}, metrics={})


@pytest.fixture(scope="module")
def cases():
    from lab9.trace_case import investigate

    return {shape: investigate(shape, "C-014", 11) for shape in ("seeded_regression", "fixed")}


def test_c014_first_wrong_step_is_pre_deducted_proposal(cases):
    events = cases["seeded_regression"]["trial"]["events"]
    kinds = [e["kind"] for e in events]
    assert "refund_history" in kinds and "proposal" in kinds
    first_bad = next(e for e in events if e["kind"] == "proposal")
    assert first_bad["payload"]["amount_vnd"] == 120000          # 150000 quote - 30000 prior refund
    assert "proposal" not in [e["kind"] for e in cases["fixed"]["trial"]["events"]]


def test_c014_graders_flag_regression_and_pass_fixed(cases):
    from lab9 import graders

    bad, good = _ctx(cases["seeded_regression"]), _ctx(cases["fixed"])
    assert graders.RefundAmountCorrect().evaluate(bad).value is False      # ledger 90000 != 120000
    assert graders.ReplyAmountAccurate().evaluate(bad).value is False      # reply 120000 != ledger 90000
    assert graders.QuoteProposalConsistent().evaluate(bad).value is False  # proposal 120000 != quote 150000
    assert graders.RefundAmountCorrect().evaluate(good).value is True
    assert graders.ReplyAmountAccurate().evaluate(good).value is True
    assert graders.QuoteProposalConsistent().evaluate(good).value is True
