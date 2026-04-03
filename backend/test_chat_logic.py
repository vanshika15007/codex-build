from chat_logic import build_rule_based_response


def test_math_applications_query_is_not_misrouted_to_admissions():
    body = build_rule_based_response("Give me 5 real-world math applications")

    assert body is not None
    assert "Budgeting" in body
    assert "Admissions" not in body


def test_greeting_returns_helpful_response():
    body = build_rule_based_response("hi")

    assert body is not None
    assert "I can help" in body


def test_how_question_explains_capabilities():
    body = build_rule_based_response("how?")

    assert body is not None
    assert "study plans" in body.lower()
    assert "real-world applications" in body.lower()


def test_admission_keyword_still_matches_admissions_flow():
    body = build_rule_based_response("How do I apply for admission?")

    assert body is not None
    assert "Admissions are open" in body
