def cartResponseEntity(cart) -> dict:
     return {
        "id": str(cart["_id"]),
        "book_id": cart["book_id"],
        "user_id": cart["user_id"],
        "quantiy": cart["quantiy"],
        "created_at": cart["created_at"],
        "updated_at": cart["updated_at"]
    }