import ebooks_alien


if __name__ == "__main__":
    ebooks_alien.app.debug = True
    ebooks_alien.app.use_reloader = True
    ebooks_alien.app.run(host="0.0.0.0", port=5000, debug=True)
