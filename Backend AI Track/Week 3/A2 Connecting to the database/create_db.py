import sqlite3

db_file = "./Backend AI Track/Week 3/A2 Connecting to the database/tasks.db"

conn = sqlite3.connect(db_file)
cur = conn.cursor()

create_tasks_table = """
    create table if not exists tasks(
        id integer primary key,
        title text not null,
        done integer not null default 0
    )
"""

count_exist_data = "select count(*) from tasks"

cur.execute(create_tasks_table)
cur.execute(count_exist_data)

count = cur.fetchone()[0]

if count == 0:
    example_tasks = [("Wake up", 1), ("Make a cup of coffee", 0), ("Eat breakfast", 0)]
    cur.executemany("insert into tasks (title, done) values (?, ?)", example_tasks)
    print("Done insertion 3 sample tasks (seeds)")

else:
    print(f"Exist {count} rows - skipping seed")

conn.commit()
conn.close()


# run : python ./"Backend AI Track"/"Week 3"/"A2 Connecting to the database"/create_db.py