"""Router rules must stay inspectable. Run: python -m pytest -q experiments/schumann-sft/test_router.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from router import route


def test_month_questions_go_to_adapter():
    for q in ("What were the mean mode centre frequencies (NS) in 2013-06?",
              "When in the day did mode 1 peak in October 2013?",
              "How high did Kp get in 2017-01?",
              "Give the average mode 1, 2 and 3 frequencies for March 2013."):
        assert route(q) == "adapter", q


def test_knowledge_base_questions_go_to_context():
    for q in ("Why does the data stop at 25 Hz?",
              "What is the calibration function Scal(f)?",
              "Is chimney_model a measurement?",
              "How do I join the tables?",
              "What licence covers the raw archive?"):
        assert route(q) == "context", q


def test_month_without_a_statistic_is_a_kb_question():
    for q in ("How many 10-minute slots does October 2013 have per sensor?",
              "Which paper covers the March 2013 recordings?"):
        assert route(q) == "context", q


def test_kb_dated_facts_stay_in_context():
    assert route("When did the Kp 7.7 storm happen, 2013-10-02?") == "context"
