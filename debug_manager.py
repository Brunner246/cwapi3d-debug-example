class DebugManager:
    """Singleton to manage debug state across the plugin
    https://refactoring.guru/design-patterns/singleton/python/example
    """
    _instance = None

    def __init__(self):
        self._debug_enabled: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DebugManager, cls).__new__(cls)
            cls._instance._debug_enabled = False
        return cls._instance

    @property
    def debug_enabled(self):
        return self._debug_enabled

    @debug_enabled.setter
    def debug_enabled(self, value):
        self._debug_enabled = bool(value)

    def enable_debug(self):
        self._debug_enabled = True

    def disable_debug(self):
        self._debug_enabled = False
