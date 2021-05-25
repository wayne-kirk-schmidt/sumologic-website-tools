#!/usr/bin/env bash

help_site="help.sumologic.com"
help_url="https://${help_site}"
help_dir="/var/tmp"

cd ${help_dir}

options="--mirror --convert-links --adjust-extension --page-requisites --no-parent"
echo ${help_site} | xargs -P 8 -I{} wget ${options} -P $help_dir/$help_site {}
