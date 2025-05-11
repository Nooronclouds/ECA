from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_product_details

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

@app.route("/api/product", methods=["GET"])
def search_product():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Product name is required"}), 400

    try:
        products = get_product_details(name)
        if not products:
            return jsonify({"message": "No products found matching your search"}), 200
        
        return jsonify(products[0])  # Return first match
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)