BIN=dist


all: $(BIN)/noop $(BIN)/zombie $(BIN)/snooze $(BIN)/factorial $(BIN)/busy $(BIN)/search

$(BIN)/noop: noop.py
	pyinstaller --onefile --log-level ERROR -p . noop.py

clean::
	-@rm -f $(BIN)/noop

$(BIN)/zombie: zombie.py
	pyinstaller --onefile --log-level ERROR -p . zombie.py

clean::
	-@rm -f $(BIN)/zombie

$(BIN)/snooze: snooze.py
	pyinstaller --onefile --log-level ERROR -p . snooze.py

clean::
	-@rm -f $(BIN)/snooze

$(BIN)/factorial: factorial.py
	pyinstaller --onefile --log-level ERROR -p . factorial.py

clean::
	-@rm -f $(BIN)/factorial

$(BIN)/busy: busy.py
	pyinstaller --onefile --log-level ERROR -p . busy.py

clean::
	-@rm -f $(BIN)/busy

$(BIN)/search: search.py
	pyinstaller --onefile --log-level ERROR -p . search.py

clean::
	-@rm -f $(BIN)/search

clean::
	-@rm -rf *.spec __pycache__
	-@ansar -f destroy
