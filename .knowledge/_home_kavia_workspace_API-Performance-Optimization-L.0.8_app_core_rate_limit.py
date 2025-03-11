{"is_source_file": true, "format": "Python", "description": "This module implements a Redis-based rate limiting functionality using FastAPI. It defines a singleton class for the rate limiter, configuration for rate limits, and an API decorator for applying rate limiting to endpoints.", "external_files": ["app/core/cache", "app/core/config"], "external_methods": ["redis.asyncio", "fastapi.Depends", "fastapi.HTTPException", "fastapi.Request", "fastapi.status", "fastapi.responses.JSONResponse"], "published": ["rate_limiter", "rate_limit", "get_rate_limiter", "get_rate_limit_dependency"], "classes": [{"name": "RateLimitConfig", "description": "A data class representing the configuration for rate limiting, with parameters for requests, period duration, and Redis key prefix."}, {"name": "RateLimiter", "description": "A singleton class that manages the rate limiting logic using Redis, ensuring only one instance exists throughout the application."}, {"name": "RateLimitDependency", "description": "A class providing a dependency for FastAPI that enforces rate limits on incoming requests based on configuration."}], "methods": [{"name": "\"RateLimiter\" __new__(cls)", "description": "Overrides the new method to ensure the RateLimiter class is a singleton.", "scope": "RateLimiter", "scopeKind": "class"}, {"name": "None initialize(self)", "description": "Initializes the rate limiter, setting up connections or any required setup actions.", "scope": "RateLimiter", "scopeKind": "class"}, {"name": "None close(self)", "description": "Cleans up the rate limiter, setting initialized state to false.", "scope": "RateLimiter", "scopeKind": "class"}, {"name": "redis.Redis client(self)", "description": "Property that returns the Redis client used for handling rate limiting operations.", "scope": "RateLimiter", "scopeKind": "class"}, {"name": "Tuple[bool,int,int] is_rate_limited( self, key: str, config: RateLimitConfig )", "description": "Checks if a particular request is rate limited based on the provided key and configuration.", "scope": "RateLimiter", "scopeKind": "class"}, {"name": "str get_client_identifier(self, request: Request)", "description": "Generates a unique identifier for a client based on their IP and user agent.", "scope": "RateLimiter", "scopeKind": "class"}, {"name": "Callable rate_limit( requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )", "description": "A decorator for applying rate limiting to FastAPI endpoint functions.", "scope": "", "scopeKind": ""}, {"name": "RateLimiter get_rate_limiter()", "description": "Provides the global rate limiter instance as a dependency.", "scope": "", "scopeKind": ""}, {"name": "None disable_for_testing(cls, disabled: bool = True)", "description": "A class method allowing the disabling of rate limiting for testing purposes.", "scope": "RateLimitDependency", "scopeKind": "class"}, {"name": "bool is_testing_disabled(cls)", "description": "Checks if rate limiting is disabled for testing.", "scope": "RateLimitDependency", "scopeKind": "class"}, {"name": "\"RateLimitDependency\" create( cls, requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )", "description": "Creates a new RateLimitDependency instance configured with the provided parameters.", "scope": "RateLimitDependency", "scopeKind": "class"}, {"name": "__init__( self, requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )", "description": "Initializes the rate limit dependency with specific requests, period, and prefix for Redis.", "scope": "RateLimitDependency", "scopeKind": "class"}, {"name": "None __call__(self, request: Request)", "description": "Checks if the incoming request should be rate limited and raises an HTTPException if the limit is exceeded.", "scope": "RateLimitDependency", "scopeKind": "class"}, {"name": "Callable get_rate_limit_dependency( requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )", "description": "Creates a callable rate limit dependency for use with FastAPI's dependency injection.", "scope": "", "scopeKind": ""}, {"name": "Callable decorator(func: Callable)", "scope": "rate_limit", "scopeKind": "function", "description": "unavailable"}, {"name": "Any wrapper(request: Request, *args: Any, **kwargs: Any)", "scope": "rate_limit.decorator", "scopeKind": "function", "description": "unavailable"}], "calls": ["logger.info", "logger.error", "inspect.signature", "asyncio.pipeline", "redis_cache.client", "functools.wraps"], "search-terms": ["Redis", "RateLimiter", "RateLimitConfig", "RateLimitDependency"], "state": 2, "file_id": 29, "knowledge_revision": 181, "git_revision": "a15e52cdf83686d94b96d45a1957085ae53f782e", "revision_history": [{"65": ""}, {"111": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"112": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"125": "db26009eb51c1d1e59dfe8e186759e95d4f68e57"}, {"178": "a15e52cdf83686d94b96d45a1957085ae53f782e"}, {"181": "a15e52cdf83686d94b96d45a1957085ae53f782e"}], "ctags": [{"_type": "tag", "name": "RateLimitConfig", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^class RateLimitConfig:$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "RateLimitDependency", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^class RateLimitDependency:$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "RateLimiter", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^class RateLimiter:$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "__call__", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    async def __call__(self, request: Request) -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "member", "signature": "(self, request: Request)", "scope": "RateLimitDependency", "scopeKind": "class"}, {"_type": "tag", "name": "__init__", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def __init__($/", "language": "Python", "kind": "member", "signature": "( self, requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )", "scope": "RateLimitDependency", "scopeKind": "class"}, {"_type": "tag", "name": "__new__", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def __new__(cls) -> \"RateLimiter\":$/", "language": "Python", "typeref": "typename:\"RateLimiter\"", "kind": "member", "signature": "(cls)", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "_initialized", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    _initialized: bool = False$/", "language": "Python", "typeref": "typename:bool", "kind": "variable", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "_instance", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    _instance: Optional[\"RateLimiter\"] = None$/", "language": "Python", "typeref": "typename:Optional[\"RateLimiter\"]", "kind": "variable", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "_testing_disabled", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    _testing_disabled = False$/", "language": "Python", "kind": "variable", "scope": "RateLimitDependency", "scopeKind": "class"}, {"_type": "tag", "name": "client", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def client(self) -> redis.Redis:$/", "language": "Python", "typeref": "typename:redis.Redis", "kind": "member", "signature": "(self)", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "close", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    async def close(self) -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "member", "signature": "(self)", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "create", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def create($/", "language": "Python", "typeref": "typename:\"RateLimitDependency\"", "kind": "member", "signature": "( cls, requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )", "scope": "RateLimitDependency", "scopeKind": "class"}, {"_type": "tag", "name": "decorator", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def decorator(func: Callable) -> Callable:$/", "file": true, "language": "Python", "typeref": "typename:Callable", "kind": "function", "signature": "(func: Callable)", "scope": "rate_limit", "scopeKind": "function"}, {"_type": "tag", "name": "disable_for_testing", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def disable_for_testing(cls, disabled: bool = True) -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "member", "signature": "(cls, disabled: bool = True)", "scope": "RateLimitDependency", "scopeKind": "class"}, {"_type": "tag", "name": "get_client_identifier", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def get_client_identifier(self, request: Request) -> str:$/", "language": "Python", "typeref": "typename:str", "kind": "member", "signature": "(self, request: Request)", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "get_rate_limit_dependency", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^def get_rate_limit_dependency($/", "language": "Python", "typeref": "typename:Callable", "kind": "function", "signature": "( requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )"}, {"_type": "tag", "name": "get_rate_limiter", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^async def get_rate_limiter() -> RateLimiter:$/", "language": "Python", "typeref": "typename:RateLimiter", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "initialize", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    async def initialize(self) -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "member", "signature": "(self)", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "is_rate_limited", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    async def is_rate_limited($/", "language": "Python", "typeref": "typename:Tuple[bool,int,int]", "kind": "member", "signature": "( self, key: str, config: RateLimitConfig )", "scope": "RateLimiter", "scopeKind": "class"}, {"_type": "tag", "name": "is_testing_disabled", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    def is_testing_disabled(cls) -> bool:$/", "language": "Python", "typeref": "typename:bool", "kind": "member", "signature": "(cls)", "scope": "RateLimitDependency", "scopeKind": "class"}, {"_type": "tag", "name": "logger", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^logger = logging.getLogger(__name__)$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "prefix", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^    prefix: str = \"ratelimit\"$/", "language": "Python", "typeref": "typename:str", "kind": "variable", "scope": "RateLimitConfig", "scopeKind": "class"}, {"_type": "tag", "name": "rate_limit", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^def rate_limit($/", "language": "Python", "typeref": "typename:Callable", "kind": "function", "signature": "( requests: Optional[int] = None, period_seconds: Optional[int] = None, prefix: str = \"ratelimit\", )"}, {"_type": "tag", "name": "rate_limiter", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^rate_limiter = RateLimiter()$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "redis", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^import redis.asyncio as redis$/", "language": "Python", "kind": "namespace", "nameref": "module:redis.asyncio"}, {"_type": "tag", "name": "wrapper", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "pattern": "/^        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:$/", "file": true, "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "(request: Request, *args: Any, **kwargs: Any)", "scope": "rate_limit.decorator", "scopeKind": "function"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/core/rate_limit.py", "hash": "23058dd1d95ec7d5cc5d6bf1ef810e65", "format-version": 4, "code-base-name": "default", "fields": [{"name": "bool _initialized", "scope": "RateLimiter", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[\"RateLimiter\"] _instance", "scope": "RateLimiter", "scopeKind": "class", "description": "unavailable"}, {"name": "_testing_disabled = False", "scope": "RateLimitDependency", "scopeKind": "class", "description": "unavailable"}, {"name": "logger = logging.getLogger(__name__)", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "str prefix", "scope": "RateLimitConfig", "scopeKind": "class", "description": "unavailable"}, {"name": "rate_limiter = RateLimiter()", "scope": "", "scopeKind": "", "description": "unavailable"}]}