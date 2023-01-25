def bookEntity(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "summary": book["summary"],
        "description": book["description"],
        "price": book["price"],
        "created_at": book["created_at"],
        "updated_at": book["updated_at"]
    }


def bookResponseEntity(book) -> dict:
     return {
        "id": str(book["_id"]),
        "title": book["title"],
        "image": book["image"],
        "summary": book["summary"],
        "description": book["description"],
        "price": book["price"],
        "created_at": book["created_at"],
        "updated_at": book["updated_at"]
    }