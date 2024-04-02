from flask import Flask, render_template, request
import jwt
import datetime as dt
import os

app = Flask(__name__)
jwtPassword = os.urandom(24).hex()
with open("flag.txt") as f:
    FLAG = f.read().strip()


@app.route("/")
def hello_world():
    expieryDate = dt.datetime.now() - dt.timedelta(minutes=5)
    payload = {"user": "guest", "exp": expieryDate}
    guest_token = jwt.encode(payload, jwtPassword, algorithm="HS256")

    user = "unknown"
    flag = None

    if token := request.args.get("token"):
        try:
            decoded = jwt.decode(
                token,
                jwtPassword,
                algorithms=["HS256"],
                options={"verify_exp": True, "verify_signature": False},
            )
            if decoded["user"] == "admin":
                user = "admin"
                flag = FLAG
            elif decoded["user"] == "guest":
                user = "guest"
        except Exception as e:
            print(e)

    return render_template("index.html", guest_token=guest_token, user=user, flag=flag)


if __name__ == "__main__":
    app.run(debug=True)
