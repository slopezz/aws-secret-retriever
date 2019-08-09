.PHONY: all build tag push bash create-secret get-secret clean help

MKFILE_PATH  := $(abspath $(lastword $(MAKEFILE_LIST)))
THISDIR_PATH := $(patsubst %/,%,$(abspath $(dir $(MKFILE_PATH))))
PROJECT_PATH := $(patsubst %/,%,$(dir $(MKFILE_PATH)))

.DEFAULT_GOAL := help

NAME ?= aws-secret-retriever
NAMESPACE ?= slopezz
VERSION ?= v1.0.0 

SECRET_NAME ?= example-ocp-cluster-ansible-vault
SECRET_KEY ?= example-ocp-cluster-ansible-vault
SECRET_VALUE ?= 123456789
REGION ?= us-east-1

LOCAL_IMAGE := $(NAME):$(VERSION)
REMOTE_IMAGE := $(NAMESPACE)/$(LOCAL_IMAGE)

all: build tag push

build: ## Build docker image. Name will be LOCAL_IMAGE=$(NAME):$(VERSION)
	docker build --file $(THISDIR_PATH)/Dockerfile -t $(LOCAL_IMAGE) $(PROJECT_PATH)

tag: ## Tag docker image
	docker tag $(LOCAL_IMAGE) $(REMOTE_IMAGE)

push: ## Push docker image to the docker registry
	docker push $(REMOTE_IMAGE)

bash: ## Start bash on built image
	docker run -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID --rm -it -u 10000001 --network host --name $(NAME) --entrypoint=/bin/bash $(LOCAL_IMAGE)

create-secret: ## Create a secret on AWS Secret Manager service
	docker run --rm -it -u 10000001 -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID $(LOCAL_IMAGE) set --secret-name $(SECRET_NAME) --secret-key $(SECRET_KEY) --secret-value $(SECRET_VALUE) --region $(REGION)

get-secret: ## Get a value from a secret stored on AWS Secret Manager Service
	docker run --rm -it -u 10000001 -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID $(LOCAL_IMAGE) get value $(SECRET_NAME) --region $(REGION)

clean: ## Clean local environment
	docker rmi $(LOCAL_IMAGE)

# Check http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
