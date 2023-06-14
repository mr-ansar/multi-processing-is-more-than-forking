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

'''Accept integer y and return the factorial(y).

int factorial(int y) {
	if (y == 0)
		return 1;
	return y * factorial(y - 1);
}

Use this process to implement recursive approach
to the calculation of factorial.
'''

import ansar.create as ar
from lib.factorial_if import FactorialReturned

# A standard component.

def factorial(self, settings, input):
	self.console('factorial({n})'.format(n=input))
	if input == 0:
		return FactorialReturned(value=1)

	a = self.create(ar.Process, 'factorial', input=input - 1)
	m = self.select(ar.Completed, ar.Stop)

	if isinstance(m, ar.Completed):
		r = m.value
		if isinstance(r, FactorialReturned):
			r = input * r.value
			return FactorialReturned(value=r)
		return r

	self.send(ar.Stop(), a)		# Child still working, initiate stop.
	self.select(ar.Completed)	# Wait for termination.
	return ar.Aborted()			# Proper stop protocol.

ar.bind(factorial)

#
#
default_input = 5

if __name__ == '__main__':
	ar.create_object(factorial, factory_input=default_input)
