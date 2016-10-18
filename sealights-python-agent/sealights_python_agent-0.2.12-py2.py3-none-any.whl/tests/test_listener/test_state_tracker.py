from python_agent.test_listener.state_tracker import StateTracker


def test_singleton(mocker):
    state_tracker1 = StateTracker()
    state_tracker2 = StateTracker()
    assert state_tracker1 == state_tracker2
    state_tracker1.current_test_identifier = "id1"
    assert state_tracker2.current_test_identifier == "id1"
    assert StateTracker().current_test_identifier == "id1"
    state_tracker1.current_test_identifier = None


def test_identifier_changing(mocker):
    mock_signal_send = mocker.patch('python_agent.packages.blinker.base.Signal.send')
    state_tracker1 = StateTracker()
    state_tracker1.current_test_identifier = None
    assert mock_signal_send.call_count == 0

    state_tracker1.current_test_identifier = "1"
    assert mock_signal_send.call_count == 1

    state_tracker1.current_test_identifier = "1"
    assert mock_signal_send.call_count == 1

    state_tracker1.current_test_identifier = "2"
    assert mock_signal_send.call_count == 2
