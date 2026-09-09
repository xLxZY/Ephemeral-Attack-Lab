output "network_name" {
  value = docker_network.lab.name
}

output "attacker_name" {
  value = docker_container.attacker.name
}

output "attacker_ip" {
  value = var.attacker_ip
}

output "target_name" {
  value = docker_container.target.name
}

output "target_ip" {
  value = var.target_ip
}
