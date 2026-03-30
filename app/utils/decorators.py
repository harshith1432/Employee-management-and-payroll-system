from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError, WrongTokenError

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims.get("role") == "admin":
                    return fn(*args, **kwargs)
                return jsonify(msg="ADMINISTRATIVE CLEARANCE REQUIRED"), 403
            except (NoAuthorizationError, InvalidHeaderError, WrongTokenError):
                return jsonify(msg="SESSION EXPIRED: PLEASE RE-AUTHENTICATE"), 401
            except Exception as e:
                # Re-raise internal server errors rather than mask as 401
                raise e
        return decorator
    return wrapper

def hr_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims.get("role") in ["admin", "hr"]:
                    return fn(*args, **kwargs)
                return jsonify(msg="HR SPECIALIST ACCESS REQUIRED"), 403
            except (NoAuthorizationError, InvalidHeaderError, WrongTokenError):
                return jsonify(msg="SESSION EXPIRED: PLEASE RE-AUTHENTICATE"), 401
            except Exception as e:
                # Re-raise internal server errors rather than mask as 401
                raise e
        return decorator
    return wrapper

def employee_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return fn(*args, **kwargs)
            except (NoAuthorizationError, InvalidHeaderError, WrongTokenError):
                return jsonify(msg="SESSION EXPIRED: PLEASE RE-AUTHENTICATE"), 401
            except Exception as e:
                # Re-raise internal server errors rather than mask as 401
                raise e
        return decorator
    return wrapper
