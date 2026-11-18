import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
task_manager = Flask(__name__, template_folder=str(BASE_DIR))
DATA_FILE = BASE_DIR / "flask_app.json"


def load_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_record(category, record):
    data = load_data()
    data[category].append(record)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


@task_manager.route("/")
def home():
    return render_template("main.html")


@task_manager.route("/branch", methods=["GET", "POST"])
def branch():
    if request.method == "POST":
        save_record("branches", {
            "branch_name": request.form["branch_name"],
            "address": request.form["address"],
            "bank_manager": request.form["bank_manager"],
            "contact": request.form["contact"],
        })
        return redirect(url_for("branch"))
    return render_template("branch.html", branches=load_data()["branches"])


@task_manager.route("/client", methods=["GET", "POST"])
def client():
    if request.method == "POST":
        data = load_data()
        save_record("clients", {
            "Id": f"CL-{len(data['clients']) + 1:04d}",
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "address": request.form["address"],
            "contact": request.form["contact"],
            "gender": request.form["gender"],
        })
        return redirect(url_for("client"))
    return render_template("client.html", clients=load_data()["clients"])


@task_manager.route("/accounts", methods=["GET", "POST"])
def accounts():
    data = load_data()
    if request.method == "POST":
        selected_client = next(
            client for client in data["clients"]
            if client["Id"] == request.form["client_id"]
        )
        account_number = f"ACC-{len(data['accounts']) + 1:04d}"
        save_record("accounts", {
            "account_number": account_number,
            "client_id": selected_client["Id"],
            "account_holder": f"{selected_client['first_name']} {selected_client['last_name']}",
            "account_type": request.form["account_type"],
            "branch": request.form["branch"],
            "date": request.form["date"],
        })
        return redirect(url_for("accounts"))
    return render_template(
        "accounts.html",
        clients=data["clients"],
        branches=data["branches"],
        accounts=data["accounts"],
    )


@task_manager.route("/transactions", methods=["GET", "POST"])
def transactions():
    data = load_data()
    if request.method == "POST":
        save_record("transactions", {
            "transaction_type": request.form["transaction_type"],
            "account_number": request.form["account_number"],
            "receiver_account": request.form.get("receiver_account", ""),
            "amount": request.form["amount"],
        })
        return redirect(url_for("transactions"))
    return render_template(
        "transaction.html",
        accounts=data["accounts"],
        transactions=data["transactions"],
    )


if __name__ == "__main__":
    task_manager.run(debug=True)
