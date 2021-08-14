from atgql.pyutils.did_you_mean import did_you_mean


def test_does_accept_an_empty_list():
    assert did_you_mean([]) == ''


def test_handles_single_suggestion():
    assert did_you_mean(['A']) == ' Did you mean "A"?'


def test_handles_two_suggestions():
    assert did_you_mean(['A', 'B']) == ' Did you mean "A" or "B"?'


def test_handles_multiple_suggestions():
    assert did_you_mean(['A', 'B', 'C']) == ' Did you mean "A", "B", or "C"?'


def test_limits_to_five_suggestions():
    assert (
        did_you_mean(['A', 'B', 'C', 'D', 'E', 'F']) == ' Did you mean "A", "B", "C", "D", or "E"?'
    )


def test_adds_sub_message():
    assert did_you_mean('the letter', ['A']) == ' Did you mean the letter "A"?'
