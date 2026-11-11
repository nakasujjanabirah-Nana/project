import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
task_manager = Flask(__name__, template_folder=str(BASE_DIR))


def load_json(filename, default):
    try:
        with (BASE_DIR / filename).open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default


def get_clients():
    data = load_json("client.json", [])
    if isinstance(data, dict):
        data = data.get("clients", [])
    return [client for client in data if isinstance(client, dict)]


def get_accounts():
    data = load_json("accounts.json", [])
    if isinstance(data, dict):
        data = data.get("accounts", [])
    return [account for account in data if isinstance(account, dict)]


@task_manager.route("/")
def home():
    return render_template("main.html")


@task_manager.route("/branch")
def branch():
    return render_template("branch.html")


@task_manager.route("/client")
def client():
    return render_template("client.html")


@task_manager.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html")




@task_manager.route("/transactions")
def transactions():
    return render_template("transaction.html")


if __name__ == "__main__":
    task_manager.run(debug=True)

