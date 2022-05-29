#!/usr/bin/env bash

umask 022

help_site="help.sumologic.com"
help_url="https://${help_site}"
help_dir="/var/tmp"

cd ${help_dir} || exit

options="--mirror --convert-links --adjust-extension --page-requisites --no-parent"
echo ${help_url} | xargs -P 12 -I{} wget "${options}" -P $help_dir/$help_site {}
