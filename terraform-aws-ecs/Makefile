.PHONY: all help deps plan apply destroy show force_deploy

ENV ?= ${USER}

all: help

help:
	@echo "Usage:"
	@echo "  make plan"
	@echo "  make apply"
	@echo "  make show"
	@echo "  make force_deploy"
	@echo "  make destroy"


plan: deps
	terraform get; \
	TF_VAR_environ="${ENV}" terraform plan --state=${ENV}.tfstate

apply: deps
	terraform get; \
	TF_VAR_environ="${ENV}" terraform apply --state=${ENV}.tfstate

destroy: deps
	TF_VAR_environ="${ENV}" terraform destroy --state=${ENV}.tfstate