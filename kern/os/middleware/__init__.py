try:
    from kern.os.middleware.jwt import (
        JWTMiddleware,
        TokenSource,
    )
except ImportError:

    class JWTMiddleware:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "PyJWT is not installed. Please install using `pip install 'kern[os]'` or `pip install PyJWT`"
            )

    class TokenSource:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "PyJWT is not installed. Please install using `pip install 'kern[os]'` or `pip install PyJWT`"
            )


from kern.os.middleware.trailing_slash import TrailingSlashMiddleware

__all__ = [
    name
    for name in (
        "JWTMiddleware",
        "TokenSource",
        "TrailingSlashMiddleware",
    )
    if name in globals()
]
