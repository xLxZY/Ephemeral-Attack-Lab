resource "docker_network" "lab" {
  name     = "cyberlab-${var.lab_id}"
  driver   = "bridge"
  internal = true

  ipam_config {
    subnet = var.network_subnet
  }

  labels {
    label = "cyberlab"
    value = "true"
  }

  labels {
    label = "lab_id"
    value = var.lab_id
  }

  labels {
    label = "scenario"
    value = var.scenario
  }
}
