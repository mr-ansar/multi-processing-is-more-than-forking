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

"""A demo of retry.

This just returns the signal that keeps a retry
going.
"""

import random
import ansar.create as ar

random.seed()

def one_chance_in(possibles):
    r = random.randrange(0, possibles)
    return r == 0

#
#
class SearchSettings(object):
	def __init__(self, exhaustion=50, success=20):
		self.exhaustion = exhaustion
		self.success = success

ar.bind(SearchSettings)

#
#
def search(self, settings):
	self.console('Searching...')
	if one_chance_in(settings.exhaustion):	# Very rarely - abandon all attempts.
		return ar.Exhausted()
	if one_chance_in(settings.success):		# More commonly - success.
		return ar.Ack()
	return ar.Maybe()			# Failed but everything ok - try again later.

ar.bind(search)

#
#
if __name__ == '__main__':
	ar.create_object(search, compiled_settings=SearchSettings())
