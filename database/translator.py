from . import schemas, models

def from_model_user_to_schema_user(user: models.User):
    return schemas.User(
        id=user.id,
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password
    )