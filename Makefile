# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2022
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
.SUFFIXES: .py

% : %.py
	pyinstaller --onefile --log-level ERROR -p . $<

BIN=dist


all: executable
	ansar --force --debug-level=CONSOLE deploy storage

executable: $(BIN)/noop $(BIN)/zombie $(BIN)/snooze $(BIN)/factorial $(BIN)/busy $(BIN)/server $(BIN)/client $(BIN)/analyzer


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

$(BIN)/server: server.py
	pyinstaller --onefile --log-level ERROR -p . server.py

clean::
	-@rm -f $(BIN)/server

$(BIN)/client: client.py
	pyinstaller --onefile --log-level ERROR -p . client.py

clean::
	-@rm -f $(BIN)/client

$(BIN)/analyzer: analyzer.py
	pyinstaller --onefile --log-level ERROR -p . analyzer.py

clean::
	-@rm -f $(BIN)/client

clean-dist:
	-@rm -f dist/* *.spec
	-@rm -rf __pycache__

clean:: clean-dist


clean::
	-@ansar -f destroy
