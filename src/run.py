from app import app

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    app.run(host='0.0.0.0')
