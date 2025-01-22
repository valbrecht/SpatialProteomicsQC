try:
    from .network import *
except ImportError:
    raise ImportError(
        "GUI dependencies are not installed. Install them with 'pip install \"domaps[gui]\"'"
    )
