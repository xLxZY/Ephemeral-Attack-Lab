resource "docker_image" "attacker" {
  name         = var.attacker_image
  keep_locally = true
}

resource "docker_image" "target" {
  name         = var.target_image
  keep_locally = true
}

resource "docker_container" "attacker" {
  name         = "attacker-01-${var.lab_id}"
  image        = docker_image.attacker.image_id
  hostname     = "attacker-01"
  restart      = "no"
  privileged   = false
  memory       = var.attacker_memory_mb
  memory_swap  = var.attacker_memory_mb
  cpus    = "1.0"
  network_mode = "bridge"

  env = [
    "LAB_ID=${var.lab_id}",
    "SCENARIO=${var.scenario}",
  ]

  networks_advanced {
    name         = docker_network.lab.name
    ipv4_address = var.attacker_ip
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
    label = "role"
    value = "attacker"
  }
}

resource "docker_container" "target" {
  name         = "web-01-${var.lab_id}"
  image        = docker_image.target.image_id
  hostname     = "web-01"
  restart      = "no"
  privileged   = false
  memory       = var.target_memory_mb
  memory_swap  = var.target_memory_mb
  cpus    = "1.0"
  network_mode = "bridge"

  env = [
    "LAB_ID=${var.lab_id}",
    "SCENARIO=${var.scenario}",
  ]

  networks_advanced {
    name         = docker_network.lab.name
    ipv4_address = var.target_ip
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
    label = "role"
    value = "target"
  }
}
