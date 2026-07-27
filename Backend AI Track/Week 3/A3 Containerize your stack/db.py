from dotenv import load_dotenv

import psycopg
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to your .env file, e.g.\n"
        "DATABASE_URL=postgres://postgres:dev@localhost:5432/tasks"
    )

conn = psycopg.connect(DATABASE_URL)
cur = conn.cursor()

create_tasks_table_query = """
    create table if not exists tasks (
        id serial primary key,
        title text not null,
        done boolean not null default false
    )
"""

count_existing_tasks_query = "select count(*) from tasks"
insert_task_query = "insert into tasks (title, done) values (%s, %s)"


def init_db():
    cur.execute(create_tasks_table_query)
    conn.commit()

    cur.execute(count_existing_tasks_query)
    count = cur.fetchone()[0]

    if count == 0:
        example_tasks = [
            ("Wake up early", True),
            ("Cook breakfast", False),
            ("Make a cup of coffee", False),
        ]
        cur.executemany(insert_task_query, example_tasks)
        conn.commit()
        print("Done insertion 3 sample tasks (seeds)")
    else:
        print(f"Exist {count} rows - skipping seed")


init_db()