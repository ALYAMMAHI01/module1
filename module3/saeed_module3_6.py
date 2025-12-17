from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Sample data - in a real app, this would come from a database
items = [
    {"id": i, "name": f"Item {i}", "description": f"Description for item {i}"}
    for i in range(1, 101)  # 100 items for demonstration
]

@app.route('/items')
def get_items():
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))

        # Validate parameters
        if page < 1:
            page = 1
        if size < 1 or size > 100:
            size = 10

        # Calculate pagination
        total_items = len(items)
        total_pages = math.ceil(total_items / size)
        start_index = (page - 1) * size
        end_index = start_index + size

        # Get paginated items
        paginated_items = items[start_index:end_index]

        # Create response with metadata
        response = {
            "items": paginated_items,
            "pagination": {
                "current_page": page,
                "page_size": size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }

        return jsonify(response)

    except ValueError:
        return jsonify({"error": "Invalid page or size parameter"}), 400


