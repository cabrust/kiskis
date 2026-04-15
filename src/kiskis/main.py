import pathlib
import typing

from flask import Flask, redirect, request, url_for

from kiskis import storage


def create_app():
    # Open password storage
    storage_ = storage.Storage(pathlib.Path.home() / ".kiskis_storage")
    secrets: typing.Dict = storage_.data
    app = Flask(__name__)

    @app.route("/")
    def default_route():
        return redirect("/passwords/")

    @app.route("/passwords/")
    def passwords():
        response = "<ul>" + "".join(
            [
                f"<li>Username: {item['username']}. Purpose: {item['purpose']}. Password: {item['password']}. "
                + f'<a href="{url_for("delete", username=item["username"])}">Delete.</a></li>'
                for item in secrets["passwords"]
            ]
        )

        response += f'<p><a href="{url_for("prepare")}">Add</a></p>'
        return response

    @app.route("/passwords/prepare")
    def prepare():
        return f"""
            <form action="{url_for("add")}" method="post">
                Username: <input type="text" name="username"><br/>
                Purpose: <input type="text" name="purpose"><br/>
                Password: <input type="text" name="password"><br/>
                <input type="submit" value="Add">
            </form>"""

    @app.route("/passwords/add", methods=["POST"])
    def add():
        record = {
            "username": request.values["username"],
            "purpose": request.values["purpose"],
            "password": request.values["password"],
        }
        secrets["passwords"].append(record)
        storage_.save()
        return redirect("/passwords")

    @app.route("/passwords/<username>/delete")
    def delete(username: str):
        record = next(
            (item for item in secrets["passwords"] if item["username"] == username),
            None,
        )
        secrets["passwords"].remove(record)
        storage_.save()
        return redirect("/passwords")

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
