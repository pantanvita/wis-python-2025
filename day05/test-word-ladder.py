import pytest
from word_ladder import one_letter_diff, is_valid_word, play_ladder_round

# A small mock word list for testing
word_list = {"cat", "cot", "dot", "dog", "dig", "big", "bag", "bat"}


# -------------------------
# Tests for one_letter_diff
# -------------------------

def test_one_letter_diff_true():
    assert one_letter_diff("cat", "bat") is True
    assert one_letter_diff("cot", "cat") is True
    assert one_letter_diff("dog", "dig") is True


def test_one_letter_diff_false():
    assert one_letter_diff("cat", "dog") is False  # all 3 letters changed
    assert one_letter_diff("cat", "cats") is False  # different length
    assert one_letter_diff("cat", "cat") is False   # zero letters changed


# -------------------------
# Tests for is_valid_word
# -------------------------

def test_is_valid_word_true():
    assert is_valid_word("cat", word_list) is True
    assert is_valid_word("dog", word_list) is True


def test_is_valid_word_false():
    assert is_valid_word("zzz", word_list) is False
    assert is_valid_word("apple", word_list) is False


# -------------------------
# Tests for play_ladder_round
# -------------------------

def test_play_ladder_round_correct():
    status, updated = play_ladder_round("cat", "bat", word_list)
    assert status == "correct"
    assert updated == "bat"


def test_play_ladder_round_invalid_word():
    status, updated = play_ladder_round("cat", "zzz", word_list)
    assert status == "invalid"
    assert updated == "cat"  # unchanged


def test_play_ladder_round_invalid_diff():
    status, updated = play_ladder_round("cat", "dog", word_list)
    assert status == "invalid"
    assert updated == "cat"

# -------------------------------------------------------
# Pytest hook to print test summary (passed & failed)
# -------------------------------------------------------

def pytest_terminal_summary(terminalreporter):
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))

    terminalreporter.write_line(f"\n--- Test Summary ---")
    terminalreporter.write_line(f"Tests passed: {passed}")
    terminalreporter.write_line(f"Tests failed: {failed}")

    if failed == 0:
        terminalreporter.write_line("All tests passed!")

# -------------------------------------------------------
# FINAL TEST — Runs last and prints custom summary
# -------------------------------------------------------

def test_zz_summary(request):
    """
    This test runs last (alphabetically). It prints a summary.
    """
    passed = len(request.session.stats.get("passed", []))
    failed = len(request.session.stats.get("failed", []))

    print("\n========== CUSTOM TEST SUMMARY ==========")
    print(f"Tests passed : {passed}")
    print(f"Tests failed : {failed}")
    print("-----------------------------------------")

    if failed == 0:
        print("🎉 ALL TESTS PASSED! 🎉")

    # Always succeeds so it doesn't affect result
    assert True