resource "vultr_instance" "plmn" {
    label = var.HOSTNAME
    plan = "vc2-1c-1gb"
    region = "sgp"
    os_id = "2284"
    enable_ipv6 = true
}


variable "HOSTNAME" {}