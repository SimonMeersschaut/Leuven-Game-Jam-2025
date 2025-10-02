from engine import Engine


if __name__ == "__main__":
    try:
        engine = Engine()
        engine.start()
    except Exception as e:
        input("Uncaught error: "+str(e))
        raise e