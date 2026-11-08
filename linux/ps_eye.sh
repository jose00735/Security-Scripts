#!/bin/bash

function ctrl_c(){
	echo -e "\n\n[!] Saliendo...\n"
	tput cnorm; exit
}

# Ctrl+c
trap ctrl_c INT

old_process="$(ps -eo command)"

tput civis
while true; do
	new_process="$(ps -eo command)"
	diff <(echo "$old_process") <(echo "$new_process") | grep -vE "command|procmon|kworker" | grep -vP "^[0-9\-]"
	old_process="$new_process"
done
tput cnorm
