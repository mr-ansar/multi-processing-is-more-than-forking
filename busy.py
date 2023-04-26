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

'''Build a hierarchy of managers, each performing a list of duties.

Accept a named workload and the dimensions of an organization. Or
more technically, the number of branches at each node and
the number of recursions.

A command like;

	$ PATH="dist:${PATH}" dist/busy --duties=["noop", "snooze"] --managers=3 --management-levels=5

produces a count of 484 processes.
'''

import ansar.create as ar
from lib.job_if import JobInput, JobReturned

def busy(self, settings, input):
	managers = input.managers
	management_levels = input.management_levels
	duties = input.duties

	# Initiate the processes at this node in the tree,
	# 1) list of named processes
	# 2) optional list of child nodes (recursive)

	for d in duties:
		a = self.create(ar.Process, d)
		self.assign(a, d)

	if management_levels > 1:
		for i in range(managers):
			role = 'busy-{i}'.format(i=i)
			next = JobInput(managers=managers, management_levels=management_levels - 1, duties=duties)
			a = self.create(ar.Process, 'busy', input=next, role_name=role)
			self.assign(a, role)

	# This node is now operational. Just wait for results
	# to flow in, watching for the possibility of an
	# interrupt.
	with ar.AutoStop(self):
		processes = 1			# Include this process.
		while self.working():
			m = self.select(ar.Completed, ar.Stop)

			# Interrupted. Control-c or Stop().
			if isinstance(m, ar.Stop):
				return ar.Aborted()

			# Process terminations. These breakdown into 3 general
			# categories, 1) expected results, 2) runtime problems,
			# and 3) unexpected results. This code also uses the
			# name (role) assigned to the process at creation-time
			# to fully identify what was received from who.

			r = self.debrief()		# Recover the role.
			value = m.value
			if isinstance(value, JobReturned):		# Busy executable, busy-x role.
				processes += value.processes
				continue
			elif isinstance(value, ar.Aborted):		# Signaled before framework active.
				self.warning('{name} aborted'.format(name=r))
				processes += 1
				continue
			elif isinstance(value, ar.Faulted):		# Error inside the remote process or interfacing.
				self.fault('{name} faulted - {fault}'.format(name=r, fault=str(value)))
				return value
			elif r in duties:		# No reported problem and its one of the duties.
				processes += 1		# This conveniently ignores the specific results
				continue			# as this process cannot know all the possible results
									# of all the possible duties.

			# Not a sub-busy, duty or error - report it.
			self.warning('unexpected output from {name} ({unexpected})'.format(name=r, unexpected=str(value)))

	return JobReturned(processes)

ar.bind(busy)

#
#
default_input = JobInput(duties=['noop', 'snooze', 'factorial'])

if __name__ == '__main__':
	ar.create_object(busy, compiled_input=default_input)
