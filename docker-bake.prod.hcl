# docker-bake.dev.hcl: allow docker buildx to build multiple files, with platforms options and push to hub
# More info: https://crazymax.dev/docker-allhands2-buildx-bake/?f=4#8

group "quickread-postgres" {
  targets = ["nginx-sever", "flask-app"]
}

target "flask-app" {
  context = "./services/flaskapp"
  dockerfile = "Dockerfile.prod"
  platforms = ["linux/amd64", "linux/arm64"]
  tags = ["docker.io/sophietruong92/quick-read-flaskapp:1.0"]
}

target "nginx-server" {
  context ="./services/nginx"
  dockerfile = "Dockerfile"
  platforms = ["linux/amd64", "linux/arm64"]
  tags = ["docker.io/sophietruong92/quick-read-webserver:1.0"]
}