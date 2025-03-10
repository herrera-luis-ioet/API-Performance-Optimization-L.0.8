{"is_source_file": true, "format": "Python", "description": "Main module that sets up and configures a FastAPI application, including middleware, exception handlers, and routing.", "external_files": ["app/api/v1/api", "app/core/config", "app/db/session"], "external_methods": ["app.api.v1.api.api_router", "app.core.config.settings", "app.db.session.init_db", "app.db.session.engine"], "published": ["app"], "classes": [], "methods": [{"name": "FastAPI create_application()", "description": "Creates and configures the FastAPI application.", "scope": "", "scopeKind": ""}, {"name": "JSONResponse http_exception_handler( request: Request, exc: StarletteHTTPException )", "description": "Handles HTTP exceptions and returns appropriate JSON responses.", "scope": "create_application", "scopeKind": "function"}, {"name": "JSONResponse validation_exception_handler( request: Request, exc: RequestValidationError )", "description": "Handles validation exceptions and returns error details in JSON format.", "scope": "create_application", "scopeKind": "function"}, {"name": "Dict[str,Any] root()", "description": "Root endpoint that provides basic API information.", "scope": "create_application", "scopeKind": "function"}, {"name": "None startup_db_client()", "description": "Initializes the database on application startup.", "scope": "", "scopeKind": ""}, {"name": "None shutdown_db_client()", "description": "Closes database connections when the application shuts down.", "scope": "", "scopeKind": ""}], "calls": ["logging.basicConfig", "FastAPI", "application.add_middleware", "application.include_router", "application.exception_handler", "logger.error", "JSONResponse", "application.get", "init_db", "await engine.dispose"], "search-terms": ["FastAPI application setup", "initialization", "middleware configuration", "API routing", "exception handling"], "state": 2, "file_id": 10, "knowledge_revision": 37, "git_revision": "c20e433ceac4b268af80c09bdfd81759d701e9ea", "revision_history": [{"21": ""}, {"35": "c20e433ceac4b268af80c09bdfd81759d701e9ea"}, {"36": "c20e433ceac4b268af80c09bdfd81759d701e9ea"}, {"37": "c20e433ceac4b268af80c09bdfd81759d701e9ea"}], "ctags": [{"_type": "tag", "name": "StarletteHTTPException", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^from starlette.exceptions import HTTPException as StarletteHTTPException$/", "language": "Python", "kind": "unknown", "nameref": "unknown:HTTPException"}, {"_type": "tag", "name": "app", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^app = create_application()$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "create_application", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^def create_application() -> FastAPI:$/", "language": "Python", "typeref": "typename:FastAPI", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "http_exception_handler", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^    async def http_exception_handler($/", "file": true, "language": "Python", "typeref": "typename:JSONResponse", "kind": "function", "signature": "( request: Request, exc: StarletteHTTPException )", "scope": "create_application", "scopeKind": "function"}, {"_type": "tag", "name": "logger", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^logger = logging.getLogger(__name__)$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "root", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^    def root() -> Dict[str, Any]:$/", "file": true, "language": "Python", "typeref": "typename:Dict[str,Any]", "kind": "function", "signature": "()", "scope": "create_application", "scopeKind": "function"}, {"_type": "tag", "name": "shutdown_db_client", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^async def shutdown_db_client() -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "startup_db_client", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^async def startup_db_client() -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "validation_exception_handler", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "pattern": "/^    async def validation_exception_handler($/", "file": true, "language": "Python", "typeref": "typename:JSONResponse", "kind": "function", "signature": "( request: Request, exc: RequestValidationError )", "scope": "create_application", "scopeKind": "function"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/main.py", "hash": "8f76f1c680320d7370833a2666343f06", "format-version": 4, "code-base-name": "default", "fields": [{"name": "app = create_application()", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "logger = logging.getLogger(__name__)", "scope": "", "scopeKind": "", "description": "unavailable"}]}