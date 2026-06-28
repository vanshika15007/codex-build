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


def test_data_science_roadmap_is_handled():
    body = build_rule_based_response("data science roadmap")

    assert body is not None
    assert "portfolio" in body.lower()


def test_python_query_returns_topic_response():
    body = build_rule_based_response("python")

    assert body is not None
    assert "python is a versatile language" in body.lower()


def test_machine_query_returns_topic_response():
    body = build_rule_based_response("machine")

    assert body is not None
    assert "machine learning" in body.lower() or "machine learning is" in body.lower()


def test_games_query_returns_game_response():
    body = build_rule_based_response("games")

    assert body is not None
    assert "game" in body.lower()
    assert "roadmap" in body.lower() or "project" in body.lower()


def test_interview_query_returns_interview_response():
    body = build_rule_based_response("interview prep")

    assert body is not None
    assert "interview" in body.lower()
    assert "plan" in body.lower() or "sample" in body.lower()


def test_admission_keyword_still_matches_admissions_flow():
    body = build_rule_based_response("How do I apply for admission?")

    assert body is not None
    assert "Admissions are open" in body


def test_full_stack_returns_specific_response():
    body = build_rule_based_response("full stack")

    assert body is not None
    assert "full stack" in body.lower()
    assert "front-end" in body.lower() or "frontend" in body.lower()


def test_ai_returns_specific_response():
    body = build_rule_based_response("AI")

    assert body is not None
    assert "artificial intelligence" in body.lower() or "ai" in body.lower()
    assert "python" in body.lower()


def test_climate_change_returns_solutions():
    body = build_rule_based_response("Explain climate change with actionable solutions")

    assert body is not None
    assert "renewable" in body.lower()
    assert "actionable" in body.lower() or "carbon" in body.lower()


if __name__ == "__main__":
    test_math_applications_query_is_not_misrouted_to_admissions()
    test_greeting_returns_helpful_response()
    test_how_question_explains_capabilities()
    test_admission_keyword_still_matches_admissions_flow()
    print("All tests passed!")
