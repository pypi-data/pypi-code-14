from python_agent.test_listener.events import EventsManager


def test_empty_event(mocker):
    mock_put = mocker.patch("python_agent.test_listener.events.EventsQueue.put")
    event_manager = EventsManager()
    event_manager.push_event(None)
    assert mock_put.call_count == 0


def test_queue_exception(mocker):
    mock_put = mocker.patch("python_agent.test_listener.events.EventsQueue.put")
    mock_put.side_effect = Exception
    event_manager = EventsManager()
    event_manager.push_event({"a": 1})
    assert mock_put.call_count == 1
