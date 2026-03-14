class Queries:

    CREATE_MESSAGE_TABLE = """
        CREATE TABLE IF NOT EXISTS message (
            id           INTEGER      PRIMARY KEY AUTOINCREMENT,
            user         VARCHAR(64)  NOT NULL,
            user_id      VARCHAR(9)   NOT NULL UNIQUE,
            created_date TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP,
            chain        VARCHAR(255) NOT NULL
        );
    """
    ADD_MESSAGE = "INSERT INTO message (user, user_id, updated_date, chain) VALUES (?, ?, ?, ?)"
    GET_BY_ID = "SELECT * FROM message WHERE id = ?"

    GET_ALL_ORDERED = "SELECT * FROM message ORDER BY created_date"

    UPDATE =  "UPDATE message SET chain = ? WHERE user_id = ?"

    DELETED_BY_ID = "DELETE FROM libros WHERE id = ?"