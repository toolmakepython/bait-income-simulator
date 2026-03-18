from flask import Flask

from routes.index_route import index_bp
from routes.wall_route import wall_bp
from routes.hourly_month_route import hourly_month_bp
from routes.annual_month_route import annual_month_bp
from routes.sitemap_route import sitemap_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
app.register_blueprint(wall_bp)
app.register_blueprint(hourly_month_bp)
app.register_blueprint(annual_month_bp)
app.register_blueprint(sitemap_bp)

if __name__ == "__main__":
    app.run(debug=True)