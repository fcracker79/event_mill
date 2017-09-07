import unittest


class ImportTest(unittest.TestCase):
    def test_should_pass(self):
        from event_mill.event import declarations
        from event_mill.event_source import declarations
        from event_mill.projection import declarations
        from event_mill.reactor import declarations
        from event_mill import exceptions
        pass
