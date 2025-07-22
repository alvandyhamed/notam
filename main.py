import os
import sys

from app import create_app

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5057, debug=True)