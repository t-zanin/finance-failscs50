import os
import requests
import urllib.parse
import datetime
from flask import redirect, render_template, request, session
from functools import wraps
from werkzeug.security import check_password_hash

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""
    try:
        api_key = "pk_f2a11cdf0b364ed99ce7412f242d3ed1"
        response = requests.get(f"https://cloud.iexapis.com/v1/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def get_time():
    """Get current time."""
    return datetime.datetime.now()  # Retorna o horário atual


def check_password(provided_password, hashed_password):
    """Check if the provided password matches the hashed password."""
    return check_password_hash(hashed_password, provided_password)

