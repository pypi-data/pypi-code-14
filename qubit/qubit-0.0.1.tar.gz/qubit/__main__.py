from .wsgiapp import app


def main() -> None:
    host, port = '0.0.0.0', 8888
    print(app.url_map)
    app.run(host, port, debug=True, use_reloader=False)

if __name__ == '__main__':
    main()
