# AWS Secret Retriever Docker image

* The aim of this docker image is to be able to create secrets on AWS Secrets Manager Service and retrieve its value, so this container execution can be integrated into any CICD to safely store secrets on a Cloud service without having to store secrets on a Github Repository

* It uses ENV VARS `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`, so you need to have `aws-cli` configured with valid credentials or at least to set these ENV VARS

## Usage

```bash
$ make
build                          Build docker image. Name will be LOCAL_IMAGE=$(NAME):$(VERSION)
tag                            Tag docker image
push                           Push docker image to the docker registry
bash                           Start bash on built image
create-secret                  Create a secret on AWS Secret Manager service
get-secret                     Get a value from a secret stored on AWS Secrets Manager Service
clean                          Clean local environment
help                           Print this help
```

## Examples

* Get secret failing because it does not exist yet:

```bash
$ make get-secret
docker run --rm -it -u 10000001 -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID aws-secret-retriever:v1.0.0  get value example-ocp-cluster-ansible-vault --region us-east-1
SECRET_NOT_FOUND
```

* Create secret:

```bash
$ make create-secret 
docker run --rm -it -u 10000001 -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID aws-secret-retriever:v1.0.0  set --secret-name example-ocp-cluster-ansible-vault --secret-key example-ocp-cluster-ansible-vault --secret-value 123456789 --region us-east-1
```

* Try to recreate secret, fails because it already exists:

```bash
$ make create-secret 
docker run --rm -it -u 10000001 -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID aws-secret-retriever:v1.0.0  set --secret-name example-ocp-cluster-ansible-vault --secret-key example-ocp-cluster-ansible-vault --secret-value 123456789 --region us-east-1
SECRET_ALREADY_EXISTS
make: *** [Makefile:36: create-secret] Error 255
```

* Get secret value:

```bash
$ make get-secret
docker run --rm -it -u 10000001 -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID aws-secret-retriever:v1.0.0  get value example-ocp-cluster-ansible-vault --region us-east-1
123456789
```

## Docker images

* Docker images will be available with specific aws-secret-retriever versions on [docker Hub](https://cloud.docker.com/repository/docker/slopezz/aws-secret-retriever/tags)
