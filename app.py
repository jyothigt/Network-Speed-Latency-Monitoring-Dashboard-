from flask import Flask, render_template, redirect, url_for
import sqlite3
import speedtest
from datetime import datetime
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

DATABASE = "network_monitor.db"


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS speed_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            download_speed REAL,
            upload_speed REAL,
            ping REAL,
            status TEXT,
            test_time TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_network_status(download_speed, upload_speed, ping):
    if download_speed >= 50 and upload_speed >= 10 and ping <= 50:
        return "Good"
    elif download_speed >= 20 and upload_speed >= 5 and ping <= 100:
        return "Average"
    else:
        return "Poor"


def get_history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT download_speed, upload_speed, ping, status, test_time
        FROM speed_tests
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows[::-1]


def create_graph():
    rows = get_history()

    if not rows:
        return

    times = [row[4] for row in rows]
    download = [row[0] for row in rows]
    upload = [row[1] for row in rows]
    ping = [row[2] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.plot(times, download, marker='o', label="Download Speed Mbps")
    plt.plot(times, upload, marker='o', label="Upload Speed Mbps")
    plt.plot(times, ping, marker='o', label="Ping ms")

    plt.xlabel("Test Time")
    plt.ylabel("Value")
    plt.title("Network Performance History")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    if not os.path.exists("static"):
        os.makedirs("static")

    plt.savefig("static/graph.png")
    plt.close()


@app.route("/")
def home():
    create_graph()
    history = get_history()
    latest = history[-1] if history else None

    return render_template("index.html", history=history, latest=latest)


@app.route("/run-test")
def run_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = round(st.download() / 1_000_000, 2)
        upload_speed = round(st.upload() / 1_000_000, 2)
        ping = round(st.results.ping, 2)

        status = get_network_status(download_speed, upload_speed, ping)
        test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO speed_tests
            (download_speed, upload_speed, ping, status, test_time)
            VALUES (?, ?, ?, ?, ?)
        """, (download_speed, upload_speed, ping, status, test_time))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Error:", e)

    return redirect(url_for("home"))


if __name__ == "__main__":
    create_table()
    app.run(debug=True)