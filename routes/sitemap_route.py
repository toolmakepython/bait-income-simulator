from flask import Blueprint, render_template, Response

sitemap_bp = Blueprint("sitemap", __name__)

@sitemap_bp.route("/sitemap.xml")
def sitemap():
    xml = render_template("sitemap.xml")
    return Response(xml, mimetype="application/xml")