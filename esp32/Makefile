.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "Available tasks:"
	@echo "    shell  Start an remote shell session"
	@echo "    sync   Copy all *.py files to the device"
	@echo "    reset  Soft reboot the board"
	@echo "    repl   Start a REPL session"
	@echo ""


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

repl:
	rshell --buffer-size 512 --port ${PORT} repl

reset:
	rshell --buffer-size 512 --port ${PORT} --timing repl "~ import machine ~ machine.reset()~"

reset_stay:
	rshell --buffer-size 512 --port ${PORT} --timing repl "~ import machine ~ machine.reset()"

.PHONY: help shell repl reset sync reset_stay
