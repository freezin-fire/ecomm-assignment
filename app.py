import os
import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_NAME = "ecommerce.db"


# def normalize_image_url(url):
#     if not url:
#         return "/static/images/placeholder.svg"
#     clean = str(url).strip()
#     if clean.startswith("./"):
#         clean = clean[1:]
#     elif not clean.startswith("/") and not clean.startswith("http://") and not clean.startswith("https://"):
#         clean = "/" + clean
#     return clean

def get_db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, DB_NAME)
    from init_db import init_db

    if not os.path.exists(db_path):
        print("Database not found. Initializing now...")
        init_db()
    else:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), image_url FROM products LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            if not row or row[0] < 30 or row[1].startswith("http") or row[1].startswith("./"):
                print("Database contains outdated product entries or image paths. Re-initializing...")
                init_db()
        except Exception as e:
            print(f"Database check failed: {e}. Re-initializing...")
            init_db()


# Frontend Page Routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product/<int:product_id>")
def product_details_page(product_id):
    return render_template("product.html", product_id=product_id)


# Backend REST API Endpoints

@app.route("/api/products", methods=["GET"])
def get_products():
    search_query = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT id, name, description, price, category, image_url, rating FROM products WHERE 1=1"
    params = []

    if search_query:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        wildcard = f"%{search_query}%"
        params.extend([wildcard, wildcard])

    if category and category.lower() != "all":
        sql += " AND LOWER(category) = LOWER(?)"
        params.append(category)

    sql += " ORDER BY id ASC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        prod = dict(row)
        # prod["image_url"] = normalize_image_url(prod["image_url"])
        products.append(prod)

    return jsonify({
        "success": True,
        "count": len(products),
        "products": products
    }), 200


@app.route("/api/products/featured", methods=["GET"])
def get_featured_products():
    exclude_id = request.args.get("exclude", type=int, default=0)

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT id, name, description, price, category, image_url, rating FROM products WHERE id != ? ORDER BY RANDOM() LIMIT 5"
    cursor.execute(sql, (exclude_id,))
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        prod = dict(row)
        # prod["image_url"] = normalize_image_url(prod["image_url"])
        products.append(prod)

    return jsonify({
        "success": True,
        "count": len(products),
        "products": products
    }), 200


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    if product_id <= 0:
        return jsonify({"success": False, "error": "Invalid product ID"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, description, price, category, image_url, rating FROM products WHERE id = ?",
        (product_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"success": False, "error": f"Product with ID {product_id} not found"}), 404

    prod = dict(row)
    # prod["image_url"] = normalize_image_url(prod["image_url"])

    return jsonify({"success": True, "product": prod}), 200


@app.route("/api/categories", methods=["GET"])
def get_categories():
    expected_order = [
        "Cabinet", "Motherboard", "CPU", "GPU", "RAM",
        "Keyboard", "Mouse", "Speakers", "Headphones", "Game Controllers"
    ]
    return jsonify({"success": True, "categories": expected_order}), 200


if __name__ == "__main__":
    ensure_database()
    app.run(debug=True, host="127.0.0.1", port=5000)
