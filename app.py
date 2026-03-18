from flask import Flask

from routes.index_route import index_bp
from routes.wall_route import wall_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
app.register_blueprint(wall_bp)

if __name__ == "__main__":
    app.run(debug=True)