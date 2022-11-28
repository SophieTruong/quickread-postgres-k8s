#!/bin/bash
################################################
# Sub-routines
################################################
line_break() # pretty print :)
{
    local input="$1"
    local count="$2"
    printf -v myString '%*s' "$count"
    printf '%s\n' "${myString// /$input}"
}

Help()
{
    # Display help
    echo -e "This script helps automate workflow with Docker. It help:\r
    (1) build a docker container: either with docker build or buildx,\r
    (2) push container to Docker Hub, \r
    (3) pull the image to local docker, and\r
    (4) deploy multiple containers to either local machine or cloud."
    echo
    echo    "Usage: bash build_push_docker.sh [OPTIONS] PARAMS"
    echo
    echo    "Options:"
    echo -e "-b  Run 'docker build' based on the PARAMS given. The order of PARAMS is:\r
    (1) \tpath/to/Dockerfile (e.g., services/flaskapp)\r
    (2) \tname of Dockerfile (e.g., Dockerfile)\r
    (3) \tDocker image name:tag (e.g. quickread-mvp:latest) \r
    (4 - optional) Docker Hub account (e.g. usename_123)\r
Ex: bash build_push_docker.sh -b services/flaskapp Dockerfile test:latest usename_123"
    echo
    echo -e "-X Run 'docker build buildx' based on the PARAMS given. The order of PARAMS is:\r
    (1) \tpath/to/Dockerfile (e.g., services/flaskapp)\r
    (2) \tname of Dockerfile (e.g., Dockerfile)\r
    (3) \tDocker image name:tag (e.g. quickread-mvp:latest) \r
    (4) \tDocker Hub account (e.g. usename_123)\r
    (5) \tplatform (e.g. linux/arm64,linux/amd64)\r
Ex: bash build_push_docker.sh -X services/flaskapp Dockerfile test:latest usename_123 linux/arm64,linux/amd64"
    echo
    echo -e "-d Deploy docker containers using 'docker compose -f {file_name} up -d' based on the PARAMS given. The order of PARAMS is:\r
    (1) \tcontext (e.g., default)\r
    (2) \tdocker-compose file name (e.g., docker-compose.yml)\r
    (Optional: For deploying with default-context, the required images for docker-compose need to exist locally)\r
    (3) \tDocker image name:tag from DockerHub(e.g. username_123/quickread-mvp:latest) \r
    (4) \tDocker image name:tag from DockerHub(e.g. username_123/quickread-mvp:latest) \r
Ex: bash build_push_docker.sh -d default docker-compose.prod.yml username_123/quick-read-flaskapp:1.3 username_123/quick-read-webserver:1.2"
    echo
    echo    "-h     Print this for Help."
}

build() # build (and push) docker image based on Dockerfile path
{
    echo    "cd to Dockerfile dir: $1"
    cd $1
    echo    "Current work dir: " 
    pwd
    echo
    echo    "Current working command is: "
    printf  '\t%s\n' "docker build -f $2 -t $3 ."
    docker build . -f ${2} -t ${3}
    echo
    echo $4
    if [ -n "$4" ]
    then 
        echo    "Done with build. Pushing container to Docker Hub: "
        printf  '\t%s\n' "docker login"
        printf  '\t%s\n' "docker image tag $3 $4/$3"
        printf  '\t%s\n' "docker image push $4/$3"
        echo
        docker login
        docker image tag $3 $4/$3
        docker image push $4/$3
    fi
    echo    'END'
}

buildX() # build (and push) docker image for multiple platforms based on Dockerfile path
{
    echo    "cd to Dockerfile dir: $1"
    cd $1
    echo    "Current work dir: " 
    pwd
    echo
    echo    "Commands to be run are: "
    printf  '\t%s\n' "docker login"
    printf  '\t%s\n' "docker buildx build --push --tag $4/$3 --file $2 --platform=$5 ."
    printf  '\t%s\n' "docker pull $4/$3"
    echo
    docker login
    docker buildx build --push --tag $4/$3 --file $2 --platform=$5 .
    docker pull $4/$3 #This is needed for deploying in local env
    echo    'END'
}

deploy() # using docker-compose set-up to deploy on different context
{
    echo -e "Using docker-compose integration with AWS and Azure to deploy to these cloud providers (More info: https://docs.docker.com/cloud/aci-integration/).\n
    Preprequesite to deploy to cloud: Set up docker context and AWS/Azure account."
    echo

    # Optional: if the require images for docker compose doesn't exist, then the 3rd and 4rd ARG define the images to be pulled
    line_break '--' 5;
    if [ "$#" == 4 ];then 
        echo    "Pulling 2 required images from Docker Hub: "
        echo    "docker pull $3"
        echo    "docker pull $4"
        docker pull $3
        docker pull $4
    elif [ "$#" == 3 ];then 
        echo    "Pulling 1 required image from Docker Hub: "
        echo    "docker pull $3"
        docker pull $3
    fi
    line_break '--' 5;

    # Display commands to be run
    echo -e "Commands to be run are:\n
    \tdocker images\n
    \tdocker context list\n
    \tdocker context use $1\n
    \tdocker compose -f $2 up -d"
    line_break '--' 5;
    line_break '--' 5;
    docker images
    line_break '--' 5;
    docker context list
    line_break '--' 5;
    docker context use $1
    line_break '--' 5;
    docker compose -f $2 up -d
    line_break '--' 5;
    echo "Run 'docker compose down' to stop and remove containers, networks"
    line_break '--' 5;
    echo    'END'

}

################################################
# MAIN PROGRAM
# Process input options
################################################
# Get the options
while getopts "hbXd" option; do
    case $option in
        b) # Build docker image
            line_break '--' 10;
            build $2 $3 $4 $5
            line_break '--' 10;
            exit;;
        X) # Build docker image
            line_break '--' 10;
            buildX $2 $3 $4 $5 $6
            line_break '--' 10;
            exit;;
        h) # display Help
            line_break '--' 10;
            Help
            line_break '--' 10;
            exit;;
        d) # deploy 
            line_break '--' 10;
            deploy $2 $3 $4 $5
            line_break '--' 10;
            exit;;
        \?) # Invalid option
            line_break '--' 10;
            echo "Error: Invalid option. Use flag '-h' for help"
            line_break '--' 10;
            exit;;
    esac
done