variable "lab_id" {
  type = string
}

variable "scenario" {
  type = string
}

variable "network_subnet" {
  type = string
}

variable "attacker_ip" {
  type = string
}

variable "target_ip" {
  type = string
}

variable "attacker_image" {
  type    = string
  default = "cyberlab-attacker:dev"
}

variable "target_image" {
  type    = string
  default = "cyberlab-web-01:dev"
}

variable "attacker_memory_mb" {
  type    = number
  default = 512
}

variable "target_memory_mb" {
  type    = number
  default = 1024
}
