# Author: Scott Woods <scott.18.ansar@gmail.com.com>
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

"""Terminate after a specified period.

Accept a timeout, pause for the amount of
time and then terminate. Support the stop
protocol.
"""

import ansar.create as ar
from lib.snooze_if import SnoozeSettings

# The timeout is provided in settings.
# There is no return value.
def snooze(self, settings):
	self.console('Do nothing for {seconds} seconds'.format(seconds=settings.seconds))
	self.start(ar.T1, settings.seconds)
	m = self.select(ar.T1, ar.Stop)
	if isinstance(m, ar.T1):
		return ar.Ack()

	# The component has been stopped. The
	# proper response is to follow protocol.
	return ar.Aborted()

ar.bind(snooze)

# The default settings, i.e. settings are
# not provided as a file or on stdin.
default_settings = SnoozeSettings(seconds=2.0)

if __name__ == '__main__':
	ar.create_object(snooze, factory_settings=default_settings)
