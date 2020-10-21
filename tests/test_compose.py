from context_compose import compose, impotent_manager
from contextlib import contextmanager


def test_impotent_manager():
    x = 1
    with impotent_manager():
        x += 1
    assert x == 2


def test_compose_impotent_manager():
    x = 1
    mgr1 = impotent_manager()
    mgr2 = impotent_manager()
    with compose([mgr1, mgr2]):
        x += 1
    assert x == 2