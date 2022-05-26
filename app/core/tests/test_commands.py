"""
Test custom Django management commands.
"""

from unittest.mock import patch

# call_command is a helper function that allows us to simulate or to
# actually call the command by the name, e.g. call the command we're testing.
from django.core.management import call_command
# Another Operational error that might be raised during the process
from django.db.utils import OperationalError
from django.test import SimpleTestCase
# OperationalError is one of the possibilities that might occur when we try
# to connect to the database before the database is ready.
from psycopg2 import OperationalError as Psycopg2Error


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Django command to wait for the database"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
