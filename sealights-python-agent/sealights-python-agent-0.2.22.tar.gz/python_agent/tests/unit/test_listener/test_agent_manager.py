from python_agent.test_listener.agent_manager import AgentManager


def test_singleton(mocker):
    mocker.patch("python_agent.test_listener.footprints.FootprintsManager.start", autospec=True)
    mocker.patch("python_agent.test_listener.events.EventsManager.start", autospec=True)
    mocker.patch("coverage.Coverage.start", autospec=True)
    agent_manager1 = AgentManager()
    agent_manager2 = AgentManager()
    assert agent_manager1 == agent_manager2
    agent_manager1.x = "1"
    assert agent_manager2.x == "1"
    assert AgentManager().x == "1"
