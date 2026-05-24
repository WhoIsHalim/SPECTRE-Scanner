import aiosqlite


async def init_db():
    db = await aiosqlite.connect("spectre.db")

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            port INTEGER,
            service TEXT,
            title TEXT,
            server TEXT
        )
        """
    )

    await db.commit()

    return db


async def save_result(db, result):
    await db.execute(
        """
        INSERT INTO results (
            ip,
            port,
            service,
            title,
            server
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (
            result.ip,
            result.port,
            result.service,
            result.http.title if result.http else "",
            result.http.server if result.http else ""
        )
    )

    await db.commit()