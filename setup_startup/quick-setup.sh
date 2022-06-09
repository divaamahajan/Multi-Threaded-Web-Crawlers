#!/bin/bash

SCRIPT_PATH=`realpath "${BASH_SOURCE[0]}"`
SCRIPT_DIR=`dirname ${SCRIPT_PATH}`
REQS=${SCRIPT_DIR}/requirements.txt

VIRTUAL_ENV=${HOME}/.serv-coder
REQMD5="${VIRTUAL_ENV}/reqs.txt.md5"

mkdir -p ${VIRTUAL_ENV} && touch ${REQMD5}

install_ansible_venv() {
    if md5sum --status -c ${REQMD5}; then
        echo "The ${REQMD5} MD5 sum matched"
    else
        echo "The ${REQMD5} MD5 sum did not match"
        echo "Creating a virtual env for ansible"
        python3 -m venv ${VIRTUAL_ENV} || \
        virtualenv -p python3 ${VIRTUAL_ENV}
        source ${VIRTUAL_ENV}/bin/activate && \
        pip3 install -U --no-deps -r ${REQS} && \
        md5sum ${REQS} > ${REQMD5}
    fi
}

install_ansible_venv

export PYTHONPATH=$PYTHONPATH:${SCRIPT_DIR}
echo "########################################################################"
echo "Activate dev profile by running following command"
echo "source ${VIRTUAL_ENV}/bin/activate"
echo "########################################################################"
