SERVICE_TARGET := jupyter-lab-serverless

PWD ?= pwd_unknown

MODULE_NAME = jupyter-lab-serverless
MODULE_VERSION = 1.0.3

# if vars not set specifially: try default to environment, else fixed value.
# strip to ensure spaces are removed in future editorial mistakes.
# tested to work consistently on popular Linux flavors and Mac.
ifeq ($(user),)
# USER retrieved from env, UID from shell.
HOST_USER ?= $(strip $(if $(USER),$(USER),nodummy))
HOST_UID ?= $(strip $(if $(shell id -u),$(shell id -u),4000))
else
# allow override by adding user= and/ or uid=  (lowercase!).
# uid= defaults to 0 if user= set (i.e. root).
HOST_USER = $(user)
HOST_UID = $(strip $(if $(uid),$(uid),0))
endif

# export such that its passed to shell functions for Docker to pick up.
export MODULE_NAME
export HOST_USER
export HOST_UID

.PHONY: module
module:
	python3 setup.py sdist

.PHONY: upload
upload:
	twine upload --skip-existing -u x -p x  dist/*

.PHONY: clean
clean:
	rm -rf ./build ./dist ./*.egg-info \
