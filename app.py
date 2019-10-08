import alien_ebooks


if __name__ == "__main__":
    alien_ebooks.app.debug = True
    alien_ebooks.app.use_reloader = True
    alien_ebooks.app.run(host="0.0.0.0", port=5000, debug=True)
