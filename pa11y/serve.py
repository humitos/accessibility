""" a minimal static server, primarily for performing audits

    this is not meant to be used in production, and some settings are insecure
    to game auditing metrics which will vary substantially by deployment
"""
from tornado import ioloop, web, options

options.define("port", default=8080, help="port to listen on")
options.define(
    "host", default="127.0.0.1", help="host interface to connect on (0.0.0.0 is all)"
)
options.define("path", help="the files to serve")

SETTINGS = dict(
    # enabling compression can have security impacts if not done correctly
    compress_response=True,
    # not really useful for production
    autoreload=True,
)


def make_settings(path):
    settings = dict(SETTINGS)
    if not path:
        raise RuntimeError("path is required")
    settings["static_path"] = path
    return settings


def make_app(settings):
    """create and return (but do not start) a tornado app"""
    app = web.Application(
        [
            (
                r"^/(.*)",
                web.StaticFileHandler,
                dict(path=settings["static_path"], default_filename="index.html"),
            )
        ],
        **settings
    )

    return app


def main(path, port, host):
    """start a tornado app on the desired port"""
    settings = make_settings(path)
    app = make_app(settings)
    app.listen(port, host)
    url = "http://{}:{}/".format(host, port)
    print("Watching files: \t\t{static_path}".format(**settings))
    print("Hosting site on:\t\t{}".format(url))
    print("\nPress `Ctrl+C` to stop")
    try:
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        ioloop.IOLoop.current().stop()
        print("The server was stopped")


if __name__ == "__main__":
    options.parse_command_line()
    main(
        path=options.options.path, port=options.options.port, host=options.options.host
    )