import os
from server.app import create_app

app = create_app()

if __name__ == "__main__":
    # Dev only. Production: gunicorn -w 1 --threads 4 -b 0.0.0.0:5000 "server.app:create_app()"
    app.run(host="0.0.0.0", port=int(os.getenv("SERVER_PORT", "5000")), threaded=True)
