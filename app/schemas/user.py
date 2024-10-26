def get_user_in_db(user) -> dict:
    return dict(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        hashed_credentials=user["hashed_credentials"],
        is_active=user["is_active"],
    )
