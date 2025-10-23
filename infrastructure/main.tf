provider "google" {
    project = "skillful-way-474913-j7"
    region = "europe-north1"
    zone = "europe-north1-a"
}

resource "google_compute_instance" "my_vm" {
    name = "django-shop-app-instance"
    machine_type = "e2-medium"
    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-12"
        }
    }

    network_interface {
        network = "default"
    }
}