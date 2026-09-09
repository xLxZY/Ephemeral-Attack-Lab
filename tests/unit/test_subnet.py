from cyberlab.store.metadata import ips_for_subnet, next_subnet


def test_lab001_subnet():
    assert next_subnet("lab-001") == "172.20.0.0/24"
    assert ips_for_subnet("172.20.0.0/24") == ("172.20.0.2", "172.20.0.3")


def test_lab002_subnet():
    assert next_subnet("lab-002") == "172.20.1.0/24"
