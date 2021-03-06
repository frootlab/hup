# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Frootlab
#
# This file is part of Frootlab Hup, https://www.frootlab.org/hup
#
#  Hup is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Hup is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Hup. If not, see <http://www.gnu.org/licenses/>.
#
"""Unittests for module 'hup.base.otree'."""

__copyright__ = '2019 Frootlab'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Frootlab Developers'
__email__ = 'contact@frootlab.org'
__authors__ = ['Patrick Michl <patrick.michl@frootlab.org>']

from unittest import mock
from hup.base import otree, test
from hup.typing import Method, Function
from hup.base.test import Case

#
# Test Cases
#

class TestOtree(test.ModuleTest):
    module = otree

    def test_has_base(self) -> None:
        self.assertCaseEqual(otree.has_base, [
            Case(args=(object, object), value=True),
            Case(args=(object, 'object'), value=True),
            Case(args=('object', object), value=True),
            Case(args=('object', str), value=True),
            Case(args=(object, 'str'), value=False),
            Case(args=(object, type), value=False),
            Case(args=('object', type), value=False)])

    def test_get_members(self) -> None:
        self.assertCaseContain(otree.get_members, [
            Case(args=(object, ), value='__class__'),
            Case(args=(otree, ), value='get_members'),
            Case(args=(otree, ), kwds={'classinfo': Function},
                value='get_members'),
            Case(args=(otree, ), kwds={'name': 'get_members'},
                value='get_members'),
            Case(args=(otree, ), kwds={
                'rules': {'about': lambda arg, attr: arg in attr},
                'about': 'members'}, value='get_members')])

        self.assertCaseNotContain(otree.get_members, [
            Case(args=(object, '*dummy*'), value='__class__'),
            Case(args=(otree, ), kwds={'classinfo': str},
                value='get_members'),
            Case(args=(otree, '*dummy*'), value='get_members'),
            Case(args=(otree, ), kwds={'name': 'dummy'},
                value='get_members'),
            Case(args=(otree, ), kwds={
                'rules': {'about': lambda arg, attr: arg == attr},
                'about': 'members'}, value='get_members')])

    def test_get_members_dict(self) -> None:
        self.assertCaseContain(otree.get_members_dict, [
            Case(args=(object, ), value='object.__class__'),
            Case(args=(otree, ), value='hup.base.otree.get_members'),
            Case(args=(otree, ), kwds={'classinfo': Function},
                value='hup.base.otree.get_members'),
            Case(args=(otree, ), kwds={'name': 'get_members'},
                value='hup.base.otree.get_members'),
            Case(args=(otree, ), kwds={
                'rules': {'about': lambda arg, attr: arg in attr},
                'about': 'members'}, value='hup.base.otree.get_members')])

        self.assertCaseNotContain(otree.get_members_dict, [
            Case(args=(object, '*dummy*'), value='object.__class__'),
            Case(args=(otree, ), kwds={'classinfo': str},
                value='hup.base.otree.get_members'),
            Case(args=(otree, '*dummy*'),
                value='hup.base.otree.get_members'),
            Case(args=(otree, ), kwds={'name': 'dummy'},
                value='hup.base.otree.get_members'),
            Case(args=(otree, ), kwds={
                'rules': {'about': lambda arg, attr: arg == attr},
                'about': 'members'}, value='hup.base.otree.get_members')])

    def test_get_name(self) -> None:
        self.assertCaseEqual(otree.get_name, [
            Case(args=('', ), value='str'),
            Case(args=(0, ), value='int'),
            Case(args=(object, ), value='object'),
            Case(args=(object(), ), value='object'),
            Case(args=(otree.get_name, ), value='get_name'),
            Case(args=(otree, ), value='hup.base.otree')])

    def test_get_lang_repr(self) -> None:
        self.assertCaseEqual(otree.get_lang_repr, [
            Case(args=(set(), ), value='no elements'),
            Case(args=([], ), value='no items'),
            Case(args=(['a'], ), value="item 'a'"),
            Case(args=([1, 2], ), value="items '1' and '2'"),
            Case(args=(['a', 'b'], 'or'), value="items 'a' or 'b'")])

    def test_get_summary(self) -> None:
        self.assertCaseEqual(otree.get_summary, [
            Case(args=(object, ), value=otree.get_summary(object())),
            Case(args=('summary.\n', ), value='summary')])

    def test_call_attr(self) -> None:
        self.assertCaseEqual(otree.call_attr, [
            Case(args=(otree, 'get_name', list), value='list'),
            Case(args=(otree, 'get_name', list), kwds={'test': True},
                value='list')])

    def test_get_methods(self) -> None:
        obj = mock.Mock()
        obj.geta.configure_mock(__class__=Method, name='a', group=1)
        obj.getb.configure_mock(__class__=Method, name='b', group=2)
        obj.setb.configure_mock(__class__=Method, name='b', group=2)
        names = otree.get_methods(obj, pattern='get*').keys()
        self.assertEqual(names, {'geta', 'getb'})
        names = otree.get_methods(obj, pattern='*b').keys()
        self.assertEqual(names, {'getb', 'setb'})
