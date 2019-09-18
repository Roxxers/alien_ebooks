import subredditgenerator


if __name__ == "__main__":
    subredditgenerator.app.debug = True
    subredditgenerator.app.use_reloader= True
    subredditgenerator.app.run()
