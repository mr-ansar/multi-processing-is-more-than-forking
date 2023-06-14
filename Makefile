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

# Final setup for this repo;
# - python3 -m venv .env
# - source .env/bin/activate
# - pip install pyinstaller
# - pip install ansar-create
# - make build home start
# - ansar list -l
# - ansar status -l
#
# Home processes are operational. Running a make at this point
# is an iteration of the edit-run-debug loop.
# - make

# Generate useful lists of build artefacts.
EXECUTABLES := analyzer busy client factorial noop server snooze zombie
BUILD := $(EXECUTABLES:%=dist/%)
SPEC := $(EXECUTABLES:%=%.spec)

# Separate the test roles from the others.
TESTS = test-.*

# The default target is the development loop.
all: test

# Turn a python script into an executable.
dist/% : %.py
	pyinstaller --onefile --log-level ERROR -p . $<

clean::
	-rm -rf build dist

# All the executables.
build: $(BUILD)

clean::
	-rm -f $(SPEC)

# Compose the multi-process solution. Ensure that test
# executables begin with the proper convention.
home: build
	ansar create
	ansar deploy dist
	ansar add server
	ansar add client test-client
	ansar add zombie
	ansar set retry test-client --encoding-file=client-retry
	ansar extract testing

clean::
	-rm -rf testing
	-ansar -f destroy

# Bring the composition up to operational status, i.e. every
# role except the test roles.
start:
	ansar -f start "$(TESTS)" --invert-search

# Bring down the operational roles.
stop:
	ansar -f stop "$(TESTS)" --invert-search

# The development loop.
test: build
	ansar --force --debug-level=CONSOLE deploy dist testing
	ansar run "$(TESTS)" --code-path=. --test-run
