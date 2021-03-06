# all the imports
import os
import sys
import sqlite3
import pandas as pd
from flask import Flask, g, render_template
from contextlib import closing

# Extracting name from args
dbname = sys.argv[1].split("/")[-1]


# create our little application :)
app = Flask(__name__)

# configuration
app.config.update(
    dict(
        DATABASE=str(dbname),
    )
)


def connect_db():
    return sqlite3.connect(app.config["DATABASE"])


def init_db():
    with closing(connect_db()) as db:
        db.commit()


@app.route("/")
def stacked_bar_chart():
    # Read query results into a pandas DataFrame
    con = connect_db()
    df = pd.read_sql_query("SELECT * from MASTER ORDER BY date ASC", con)

    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())

    con.close()

    date = df["date"].values.tolist()  # x axis
    commits = df["commits"].values.tolist()
    # issues = df["issues"].values.tolist()
    # lines_of_code = df["lines_of_code"].values.tolist()
    # issue_spoilage_avg = df["issue_spoilage_avg"].values.tolist()
    # issue_spoilage_min = df['issue_spoilage_min'].values.tolist()
    # issue_spoilage_max = df['issue_spoilage_max'].values.tolist()
    # defect_density = df["defect_density"].values.tolist()

    return render_template(
        "linegraph.html",
        date=date,
        commits=commits,
        issues=issues,
        lines_of_code=lines_of_code,
        defect_density=defect_density,
        issue_spoilage_avg=issue_spoilage_avg,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")

# first build the docker image
# then run 'docker run -v metrics:/metrics -p 5000:5000 <name_of_image>'
# this opens a port for the flask server to run in
