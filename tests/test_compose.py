from context_compose import compose, impotent_manager
from contextlib import contextmanager
from typing import List


def test_impotent_manager():
    """
    The impotent manager is invoked without error
    """
    x = 1
    with impotent_manager():
        x += 1
    assert x == 2


def test_compose_impotent_manager():
    """
    The impotent manager is composed twice without error
    """
    x = 1
    mgr1 = impotent_manager()
    mgr2 = impotent_manager()
    with compose([mgr1, mgr2]):
        x += 1
    assert x == 2


@contextmanager
def logging_manager(name: str, log: List[str]):
    log.append(f"Entered {name}")
    yield
    log.append(f"Exited {name}")


def test_compose_enter_order():
    """
    The compose manager enters and exits context managers in
    list order
    """
    log = []
    mgr1 = logging_manager("A", log)
    mgr2 = logging_manager("B", log)
    mgr3 = logging_manager("C", log)

    with compose([mgr1, mgr2, mgr3]):
        pass

    assert log == [
        "Entered A",
        "Entered B",
        "Entered C",
        "Exited C",
        "Exited B",
        "Exited A",
    ]


def test_compose_with_none():
    """
    Any `None` values encountered in the compose list are treated
    as impotent

    """
    log = []
    mgr1 = logging_manager("A", log)

    with compose([mgr1, None]):
        pass

    assert log == [
        "Entered A",
        "Exited A",
    ]