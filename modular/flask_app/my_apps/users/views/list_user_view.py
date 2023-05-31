from flask import request, current_app, jsonify, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from my_apps.utils.decorators import (
    x_api_key_required,
    check_unique_email,
)
from my_apps.utils.response import customResponse
from my_apps.users.models import (
    User,
    user_fields,
)
from my_apps import (
    APIView,
    db,
    pagination,
)


class ListUserView(APIView):
    parameters = [
        {
            'in': 'header',
            'name': 'x-api-key',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True,
            'description': 'Access token for authentication'
        },
    ]
    responses = {
        200: {
            "description": "Users list",
            "schema": {
                "type": "object",
                "properties": {
                    "pagination": {
                        "type": "object",
                        "properties": {
                            "current": {
                                "type": "string",
                                "description": "Current page"
                            },
                            "next": {
                                "type": "string",
                                "description": "List for next page"
                            },
                            "pages": {
                                "type": "integer",
                                "description": "Cant of pages"
                            },
                            "per_page": {
                                "type": "integer",
                                "description": "Cant of records total per page"
                            },
                            "prev": {
                                "type": "string",
                                "description": "List for previous page"
                            },
                            "total": {
                                "type": "integer",
                                "description": "Total records"
                            },
                        },
                    },
                    "results": {
                        "type": "array",
                        "items": {
                            "type":  "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "description": "User id"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "User name"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "User email"
                                },
                            },
                        },
                    }
                }
            }
        },
    }

    @jwt_required()
    @x_api_key_required
    @cross_origin(supports_credentials=True)
    def get(self):
        serialized_users = [user.as_dict() for user in User.query.order_by(User.id.asc()).all()]

        return pagination.paginate(User, user_fields,  pagination_schema_hook=lambda current_page, page_obj: {
            "next": page_obj.has_next,
            "prev": page_obj.has_prev,
            "current": current_page,
            "pages": page_obj.pages,
            "per_page": page_obj.per_page,
            "total": page_obj.total,
        })
        # return customResponse({"count": len(serialized_users), "results": serialized_users}, status=200)

