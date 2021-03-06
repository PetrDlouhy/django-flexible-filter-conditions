# -*- coding: utf-8 -*-

# Author: Petr Dlouhý <petr.dlouhy@auto-mat.cz>
#
# Copyright (C) 2017 o.s. Auto*Mat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import datetime

from django.db.models import Q
from django.test import TestCase

from freezegun import freeze_time

from model_mommy import mommy

from flexible_filter_conditions.models import Condition, TerminalCondition


class TestVariableDescription(TestCase):
    """ Test TerminalCondition.variable_description() """

    def test_return_text(self):
        """ Test if description of function is returned """
        t = mommy.make(
            "flexible_filter_conditions.TerminalCondition",
            variable="TestModel.test_field",
            condition__named_condition__name="Foo condition",
        )
        self.assertEqual(t.variable_description(), "Foo help_text")

    def test_action(self):
        """ Test actions """
        t = mommy.make(
            "flexible_filter_conditions.TerminalCondition",
            variable="action",
            condition__named_condition__name="Foo condition",
        )
        self.assertEqual(
            t.variable_description(),
            "action",
        )

    def test_variable_none(self):
        """ Test if variable is none """
        t = mommy.make(
            "flexible_filter_conditions.TerminalCondition",
            variable=None,
            condition__named_condition__name="Foo condition",
        )
        self.assertEqual(
            t.variable_description(),
            None,
        )


class TestGetQuerystring(TestCase):
    def setUp(self):
        self.t = mommy.make(
            "flexible_filter_conditions.TerminalCondition",
            condition__named_condition__name="Foo condition",
        )

    def test_equals(self):
        """ Test if '=' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", "="), "foo__bar")

    def test_notequals(self):
        """ Test if '!=' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", "!="), "foo__bar")

    def test_lt(self):
        """ Test if '<' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", "<"), "foo__bar__lt")

    def test_gt(self):
        """ Test if '>' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", ">"), "foo__bar__gt")

    def test_lte(self):
        """ Test if '<=' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", "<="), "foo__bar__lte")

    def test_gte(self):
        """ Test if '>=' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", ">="), "foo__bar__gte")

    def test_contains(self):
        """ Test if 'contains' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", "contains"), "foo__bar__contains")

    def test_icontains(self):
        """ Test if 'icontains' as @operation works """
        self.assertEqual(self.t.get_querystring("User.foo.bar", "icontains"), "foo__bar__icontains")


class BaseTestCase(TestCase):
    def assertQuerysetEquals(self, qs1, qs2):
        def pk(o):  # pragma: no cover
            return o.pk  # pragma: no cover
        return self.assertEqual(  # pragma: no cover
            sorted(qs1, key=pk),
            sorted(qs2, key=pk),
        )

    def assertQueryEquals(self, q1, q2):
        return self.assertEqual(
            q1.__str__(),
            q2.__str__(),
        )


@freeze_time("2010-1-1")
class ConditionsTests(BaseTestCase):
    """ Test conditions infrastructure and conditions in fixtures """
    maxDiff = None

    def test_datetime_condition(self):
        c = Condition.objects.create(operation="and", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.date_condition",
            value="datetime.2010-09-24 00:00",
            operation=">",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(date_condition__gt=datetime.datetime(2010, 9, 24, 0, 0)))
        self.assertQueryEquals(c.condition_string(), "(User.date_condition > datetime.2010-09-24 00:00)")

    def test_date_condition(self):
        c = Condition.objects.create(operation="and", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.date_condition",
            value="date.2010-09-24",
            operation=">",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(date_condition__gt=datetime.datetime(2010, 9, 24, 0, 0)))
        self.assertQueryEquals(c.condition_string(), "(User.date_condition > date.2010-09-24)")

    def test_boolean_condition(self):
        c = Condition.objects.create(operation="or", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.boolean_condition",
            value="true",
            operation="=",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(boolean_condition=True))
        self.assertQueryEquals(c.condition_string(), "(User.boolean_condition = true)")

    def test_list_condition(self):
        c = Condition.objects.create(operation="or", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.boolean_condition",
            value="list.3,4",
            operation="in",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(boolean_condition__in=['3', '4']))
        self.assertQueryEquals(c.condition_string(), "(User.boolean_condition in list.3,4)")

    def test_time_condition(self):
        c = Condition.objects.create(operation="or", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.time_condition",
            value="month_ago",
            operation="<",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(time_condition__lt=datetime.datetime(2009, 12, 2, 0, 0)))
        self.assertQueryEquals(c.condition_string(), "(User.time_condition < month_ago)")

    def test_text_condition(self):
        c = Condition.objects.create(operation="or", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.text_condition",
            value="asdf",
            operation="contains",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(text_condition__contains="asdf"))
        self.assertQueryEquals(c.condition_string(), "(User.text_condition contains asdf)")

    def test_text_icontains_condition(self):
        c = Condition.objects.create(operation="or", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.text_condition",
            value="asdf",
            operation="icontains",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(text_condition__icontains="asdf"))
        self.assertQueryEquals(c.condition_string(), "(User.text_condition icontains asdf)")

    def test_action_condition_equals(self):
        c = Condition.objects.create(operation="or", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="action",
            value="asdf",
            operation="=",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(action="asdf"), Q())

    def test_action_condition_not_equals(self):
        c = Condition.objects.create(operation="or", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="action",
            value="asdf",
            operation="=",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(pk__in=[]))
        self.assertQueryEquals(c.condition_string(), "(action = asdf)")

    def test_blank_condition(self):
        c = Condition.objects.create(operation="and", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.regular_payments",
            value="regular",
            operation="=",
            condition=c,
        )
        self.assertQueryEquals(c.get_query(), Q(regular_payments="regular"))
        self.assertQueryEquals(c.condition_string(), "(User.regular_payments = regular)")

    def test_combined_condition(self):
        c = Condition.objects.create(operation="and", named_condition=mommy.make("NamedCondition"))
        TerminalCondition.objects.create(
            variable="User.days_ago_condition",
            value="days_ago.6",
            operation="!=",
            condition=c,
        )
        TerminalCondition.objects.create(
            variable="User.time_condition",
            value="timedelta.5",
            operation=">=",
            condition=c,
        )
        self.assertQueryEquals(
            c.get_query(),
            ~Q(days_ago_condition=datetime.datetime(2009, 12, 26, 0, 0)) & Q(time_condition__gte=datetime.timedelta(5)),
        )
        self.assertQueryEquals(
            c.condition_string(),
            "(User.days_ago_condition != days_ago.6 and User.time_condition >= timedelta.5)",
        )

    def test_multiple_combined_conditions(self):
        c = mommy.make('NamedCondition')
        c2 = mommy.make('Condition', operation="or", negate=True, named_condition=c)
        c1 = mommy.make('Condition', operation="and", conds=c2)
        TerminalCondition.objects.create(
            variable="User.days_ago_condition",
            value="days_ago.6",
            operation="!=",
            condition=c1,
        )
        TerminalCondition.objects.create(
            variable="User.time_condition",
            value="timedelta.5",
            operation=">=",
            condition=c1,
        )
        TerminalCondition.objects.create(
            variable="User.int_condition",
            value="4",
            operation="=",
            condition=c2,
        )
        TerminalCondition.objects.create(
            variable="User.int_condition",
            value="5",
            operation="<=",
            condition=c2,
        )
        test_query = ~(
            (~Q(days_ago_condition=datetime.datetime(2009, 12, 26, 0, 0)) & Q(time_condition__gte=datetime.timedelta(5))) |
            Q(int_condition=4) | Q(int_condition__lte=5)
        )
        self.assertQueryEquals(c.conditions.first().get_query(), test_query)
        self.assertQueryEquals(
            c.condition_string(),
            "not(((User.days_ago_condition != days_ago.6 and User.time_condition >= timedelta.5) "
            "or User.int_condition = 4 or User.int_condition <= 5))",
        )
