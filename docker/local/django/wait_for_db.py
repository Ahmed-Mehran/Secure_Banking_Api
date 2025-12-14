## See this file was not created by the tutor and this whole code was part of the entrypoint.sh script. But there was an error because of this code as Chat-Gpt said that its because that this Python code 
## was being included in the Script and that is why was not working, so we made a separate .py file for it and is being called from entrypoint.sh only

import time
import sys
import psycopg2
import os

suggest_unrecoverable_after = 30
start = time.time()

while True:
    try:
        psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to become available...\n")
        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write(
                f"This is taking longer than expected, it can indicate an error: '{error}'\n"
            )
        time.sleep(3)
