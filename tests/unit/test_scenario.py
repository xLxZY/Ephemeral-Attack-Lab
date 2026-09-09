from cyberlab.scenarios.loader import load_scenario


def test_ssh_privesc_loads():
    data = load_scenario("ssh-privesc")
    assert data["target"]["hostname"] == "web-01"
    assert "writable_deployment_component" in data["vulnerabilities"]
