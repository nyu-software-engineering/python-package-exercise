from .cat import Cat, MOODS, FOODS

__all__ = ["Cat", "MOODS", "FOODS", "Window", "run"] # Lists what `from desktop_cat import *` can actually bring in. Just easier for users to install

def __getattr__(name):
    if name in ("Window", "run"):
        from . import window
        return getattr(window, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")