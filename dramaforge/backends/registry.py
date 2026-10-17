"""Backend registry.

A backend is a callable that turns ``(clean_text, tokens, attrs, turns,
speakers, config)`` into an ``AudioResult``. The registry maps names to backend
classes; ``get_backend`` instantiates with the config.
"""
_BACKENDS = {}


def register_backend(name):
    def deco(cls):
        _BACKENDS[name] = cls
        return cls
    return deco


def get_backend(name, config):
    if name not in _BACKENDS:
        raise KeyError("unknown backend %r (available: %s)"
                       % (name, ", ".join(sorted(_BACKENDS))))
    return _BACKENDS[name](config)


def list_backends():
    return sorted(_BACKENDS)
