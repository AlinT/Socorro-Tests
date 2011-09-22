#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Crash Tests Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from crash_stats_page import CrashStatsHomePage
from unittestzero import Assert

from distutils.version import LooseVersion
import re
from types import StringType, IntType

class TestLayout:

    def test_that_product_versions_are_orderd_correctly(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa, True)

        current_list = csp.current_version_list.replace('(beta)', 'b1').split()
        current_versions = [Version(curent) for curent in current_list]

        Assert.is_sorted_descending(current_versions)

        other_list = csp.other_version_list.replace('(beta)', 'b1').split()
        print other_list
        other_versions = [Version(curent) for curent in other_list]
#        other_versions.sort(reverse=True)

        for ver in other_versions:
            print ver

        Assert.is_sorted_descending(other_versions)


class Version(LooseVersion):

    def parse (self, vstring):
        self.vstring = vstring
        components = filter(lambda x: x and x != '.', self.component_re.split(vstring))
        for i in range(len(components)):
            try:
                components[i] = int(components[i])
            except ValueError:
                components[i] = components[i]

        self.version = components

    def __cmp__ (self, other):
        if isinstance(other, StringType):
            other = LooseVersion(other)

        a = self.version
        b = other.version
        while len(a) < len(b): a.append(0)
        while len(b) < len(a): b.append(0)

        for i in range(len(a)):

            if not isinstance(a[i], IntType) and isinstance(b[i], IntType):
                return -1

            if not isinstance(b[i], IntType) and isinstance(a[i], IntType):
                return 1

        #If the element from list A is greater than B,
        #versionA is greater than versionB and visa versa.
        #If they are equal, go to the next element.
            if a[i] > b[i]:
                return 1
            elif b[i] > a[i]:
                return -1
        #If we reach this point, the versions are equal
        return 0
