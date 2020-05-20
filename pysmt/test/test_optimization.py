#
# This file is part of pySMT.
#
#   Copyright 2014 Andrea Micheli and Marco Gario
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from pysmt.test import TestCase, skipIfNoOptimizerForLogic
from pysmt.test import main

from pysmt.shortcuts import Optimizer, GE, Int, Symbol, INT, LE, GT, REAL, Real
from pysmt.shortcuts import And, Plus, Minus, get_env
from pysmt.logics import QF_LIA, QF_LRA
from pysmt.optimization.goal import MaximizationGoal, MinimizationGoal, \
    MinMaxGoal, MaxMinGoal

from pysmt.exceptions import PysmtUnboundedOptimizationError

class TestOptimization(TestCase):

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_minimization_basic(self):
        x = Symbol("x", INT)
        min = MinimizationGoal(x)
        formula = GE(x, Int(10))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(formula)
                model, cost = opt.optimize(min)
                self.assertEqual(model[x], Int(10))


    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_maximization_basic(self):
        x = Symbol("x", INT)
        max = MaximizationGoal(x)
        formula = LE(x, Int(10))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(formula)
                model, cost = opt.optimize(max)
                self.assertEqual(model[x], Int(10))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_maxmin_basic_lia(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)

        f11 = GE(x, Int(5))
        f12 = LE(x, Int(8))
        f21 = GE(y, Int(11))
        f22 = LE(y, Int(14))
        f31 = GE(z, Int(15))
        f32 = LE(z, Int(18))

        maxmin = MaxMinGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(maxmin)
                self.assertEqual(model[maxmin.term()], Int(8))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_minmax_basic_lia(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)

        f11 = GE(x, Int(5))
        f12 = LE(x, Int(8))
        f21 = GE(y, Int(11))
        f22 = LE(y, Int(14))
        f31 = GE(z, Int(15))
        f32 = LE(z, Int(18))

        minmax = MinMaxGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(minmax)
                self.assertEqual(model[minmax.term()], Int(15))

    @skipIfNoOptimizerForLogic(QF_LRA)
    def test_maxmin_basic_lra(self):
        x = Symbol("x", REAL)
        y = Symbol("y", REAL)
        z = Symbol("z", REAL)

        f11 = GE(x, Real(5.0))
        f12 = LE(x, Real(8.0))
        f21 = GE(y, Real(11.0))
        f22 = LE(y, Real(14.0))
        f31 = GE(z, Real(15.0))
        f32 = LE(z, Real(18.0))

        maxmin = MaxMinGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LRA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(maxmin)
                self.assertEqual(model[maxmin.term()], Real(8.0))

    @skipIfNoOptimizerForLogic(QF_LRA)
    def test_minmax_basic_lra(self):
        x = Symbol("x", REAL)
        y = Symbol("y", REAL)
        z = Symbol("z", REAL)

        f11 = GE(x, Real(5.0))
        f12 = LE(x, Real(8.0))
        f21 = GE(y, Real(11.0))
        f22 = LE(y, Real(14.0))
        f31 = GE(z, Real(15.0))
        f32 = LE(z, Real(18.0))

        minmax = MinMaxGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LRA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(minmax)
                self.assertEqual(model[minmax.term()], Real(15.0))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_pareto(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        formula = And(GE(x, Int(0)), GE(y, Int(0)), LE(x, Int(10)), LE(y, Int(10)))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                try:
                    opt.add_assertion(formula)
                    models, costs = zip(*opt.pareto_optimize([Plus(x, y), Minus(x, y)]))
                    self.assertEqual(len(models), 11)
                    self.assertTrue(all(m[x].constant_value() == 0 for m in models))
                    self.assertTrue(all(x[0].constant_value() == -x[1].constant_value() for x in costs))
                except NotImplementedError:
                    pass # OptiMathSAT wrapping of pareto is incomplete

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_unbounded(self):
        x = Symbol("x", INT)
        formula = LE(x, Int(10))
        min = MinimizationGoal(x)
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                if opt.can_diverge_for_unbounded_cases():
                    continue
                opt.add_assertion(formula)
                with self.assertRaises(PysmtUnboundedOptimizationError):
                    opt.optimize(min)

    @skipIfNoOptimizerForLogic(QF_LRA)
    def test_infinitesimal(self):
        x = Symbol("x", REAL)
        formula = GT(x, Real(10))
        min = MinimizationGoal(x)
        for oname in get_env().factory.all_optimizers(logic=QF_LRA):
            with Optimizer(name=oname) as opt:
                if opt.can_diverge_for_unbounded_cases():
                    continue
                opt.add_assertion(formula)
                with self.assertRaises(PysmtUnboundedOptimizationError):
                    opt.optimize(min)

if __name__ == '__main__':
    main()
