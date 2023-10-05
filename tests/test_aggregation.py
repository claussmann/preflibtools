from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.aggregation import *

from unittest import TestCase


class TestAnalysis(TestCase):
    def test_borda(self):
        # 0 > 1 > 2
        # 2 > 0 > 1
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        scores = borda_scores(instance)
        assert scores[0] == 3
        assert scores[1] == 1
        assert scores[2] == 2
    
    def test_borda_weak(self):
        # 0 > 1 ~ 2 > 3
        # 2 > 0 > 3 > 1
        instance = OrdinalInstance()
        orders = [((0,), (1,2), (3,)), ((2,), (0,), (3,), (1,))]
        instance.append_order_list(orders)
        scores = borda_scores(instance)
        assert scores[0] == 5
        assert scores[1] == 1
        assert scores[2] == 4
        assert scores[3] == 1
    
    def test_borda_incomplete(self):
        # 0 > 1 ~ 2
        # 2 > 0 > 3 > 1
        instance = OrdinalInstance()
        orders = [((0,), (1,2)), ((2,), (0,), (3,), (1,))]
        instance.append_order_list(orders)
        with self.assertRaises(PreferenceIncompatibleError):
            borda_scores(instance)
    
    def test_condorcet_not_exists(self):
        # 0 > 1 > 2
        # 2 > 0 > 1
        # 1 > 2 > 0
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is False
    
    def test_condorcet_not_exists_weak(self):
        # 0 > 1 ~ 2
        # 2 > 0 > 1
        # 1 > 2 > 0
        instance = OrdinalInstance()
        orders = [((0,), (1,2)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is False
    
    def test_condorcet_exists(self):
        # 0 > 1 > 2
        # 2 > 1 > 0
        # 1 > 0 > 2
        # 1 > 2 > 0
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (1,), (0,)),
            ((1,), (0,), (2,)),
            ((1,), (2,), (0,)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is True
    
    def test_condorcet_exists_weak(self):
        # 0 > 1 > 2 ~ 3
        # 2 ~ 3 > 1 > 0
        # 1 > 0 > 2 ~ 3
        # 1 > 2 > 0 ~ 3
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,3)),
            ((2,3), (1,), (0,)),
            ((1,), (0,), (2,3)),
            ((1,), (2,), (0,3)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is True
