from qubit.io.postgres import connection, new_connection


def test_db():
    assert connection
    assert new_connection()
