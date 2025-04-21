from app.main import app
import os

if __name__ == '__main__':
    from app.main import app
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
