from importlib.metadata import Distribution

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version

try:
    from .mgz2imgslices     import mgz2imgslices
except:
    from mgz2imgslices      import mgz2imgslices
