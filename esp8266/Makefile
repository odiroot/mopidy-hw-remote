PORT="/dev/ttyUSB0"
SOURCE="./src"
VENDOR="./vendor"

get_vendor:
	wget -N -i requirements-url.txt -P ${VENDOR}

sync_vendor:
	rshell --buffer-size 512 --port ${PORT} --timing rsync ${VENDOR} /pyboard/lib

sync_code:
	rshell --buffer-size 512 --port ${PORT} --timing rsync ${SOURCE} /pyboard

sync: sync_vendor sync_code

shell:
	rshell --buffer-size 512 --port ${PORT}

reset:
	rshell --buffer-size 512 --port ${PORT} --timing repl "~ import machine ~ machine.reset()"

repl:
	mpremote

.PHONY: shell repl reset sync
