#!/bin/bash
# nmapx: two-stage nmap wrapper.
#   1) full TCP port sweep that saves grepable output
#   2) service/version + default scripts against only the open ports from stage 1

display_help() {
	echo "Usage: nmapx <ip> [option...]" >&2
	echo
	echo "   -ps, --port-scan          -sS -n -Pn --open -p- --min-rate=3000 -vvv  (saves grepable output)"
	echo "   -rs, --recognition-scan   -sCV on the open ports read from the port-scan file"
	echo "   -f,  --file <name>        output file (default: allPorts)"
	echo
	echo "   example: nmapx 10.10.10.5 -ps -f allPorts && nmapx 10.10.10.5 -rs -f allPorts"
	exit 1
}

display_error() {
	echo -e "[!] syntax error\n" >&2
	display_help
}

port_scan() {
	sudo nmap -sS -n -Pn --open -p- --min-rate=3000 -vvv "$addr" -oG "$file"
}

recognition_scan() {
	if [ ! -f "$file" ]; then
		echo "[!] $file not found: run the port scan (-ps) first" >&2
		exit 1
	fi
	ports="$(grep -oP '\d{1,5}/open' "$file" | cut -d '/' -f1 | sort -un | paste -sd ',')"
	if [ -z "$ports" ]; then
		echo "[!] no open ports in $file" >&2
		exit 1
	fi
	nmap -sCV -p"$ports" "$addr" -oN "${file}_targeted"
}

if [ $# -eq 0 ]; then
	display_help
fi

file="allPorts"

while (( "$#" )); do
	case "$1" in
		-h|--help)
			display_help
		;;
		-ps|--port-scan)
			[ -z "$mode" ] && mode="ps" || display_error
			shift
		;;
		-rs|--recognition-scan)
			[ -z "$mode" ] && mode="rs" || display_error
			shift
		;;
		-f|--file)
			if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
				file=$2
				shift 2
			else
				display_error
			fi
		;;
		*)
			if [[ $1 =~ ^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$ ]]; then
				addr=$1
			else
				display_error
			fi
			shift
		;;
	esac
done

[ -z "$addr" ] && display_error

case "$mode" in
	ps) port_scan ;;
	rs) recognition_scan ;;
	*)  display_error ;;
esac
