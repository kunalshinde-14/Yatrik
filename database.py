import oracledb

def get_connection():
    connection = oracledb.connect(
        user="system",
        password="lumos",
        dsn="localhost/XEPDB1"
    )

    return connection