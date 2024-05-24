#!/usr/bin/env python3

from app import app
import configparser

cfg = configparser.ConfigParser()
cfg.read("app.cfg")

app.secret_key = cfg.get("flask", "secret_key")

app_host: str = None
try:
    app_host = cfg.get("flask", "host")
except configparser.NoOptionError:
    pass

try:
    app.debug = True if int(cfg.get("flask", "debug")) == 1 else False
except configparser.NoOptionError:
    app.debug = False

try:
    # ProxyFix default value
    x_for = 1
    x_proto = 1
    x_host = 0
    x_port = 0
    x_prefix = 0

    try:
        x_for = int(cfg.get("proxy_fix", "x_for"))
    except configparser.NoOptionError:
        pass

    try:
        x_proto = int(cfg.get("proxy_fix", "x_proto"))
    except configparser.NoOptionError:
        pass

    try:
        x_host = int(cfg.get("proxy_fix", "x_host"))
    except configparser.NoOptionError:
        pass

    try:
        x_port = int(cfg.get("proxy_fix", "x_port"))
    except configparser.NoOptionError:
        pass

    try:
        x_prefix = int(cfg.get("proxy_fix", "x_prefix"))
    except configparser.NoOptionError:
        pass

    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=x_for, x_proto=x_proto, x_host=x_host, x_port=x_port, x_prefix=x_prefix)

except configparser.NoSectionError:
    pass


if __name__ == "__main__":
    app.run(host=app_host)
