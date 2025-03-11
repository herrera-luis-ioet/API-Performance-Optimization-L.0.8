{"is_source_file": true, "format": "Python", "description": "This module manages database sessions and connections with support for async operations, specifically targeting Amazon RDS MySQL.", "external_files": ["app/core/config", "app/db/base", "app/models/product", "app/models/order"], "external_methods": ["settings.get_database_uri", "AsyncSession.rollback", "AsyncSession.commit", "AsyncSession.close", "AsyncConnection.run_sync"], "published": [], "classes": [], "methods": [{"name": "AsyncGenerator[AsyncConnection,None] get_db_connection()", "description": "Yields a database connection from the pool for async usage.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncSession,None] get_db_session()", "description": "Yields a database session with error handling and session closure.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncSession,None] db_session()", "description": "Context manager for handling database sessions with transaction management.", "scope": "", "scopeKind": ""}, {"name": "None init_db()", "description": "Initializes the database by creating all necessary tables defined in the models.", "scope": "", "scopeKind": ""}], "calls": ["async_session_factory", "engine.begin", "logger.error", "Base.metadata.create_all"], "search-terms": ["async_database_session", "connection_pooling", "Amazon RDS MySQL"], "state": 2, "file_id": 12, "knowledge_revision": 160, "git_revision": "55848e0fcb8cce64a3da13885bd787a26402348e", "revision_history": [{"25": ""}, {"106": "4db64f9e0fb4f3f158374b1eb71593cce03b795c"}, {"155": "55848e0fcb8cce64a3da13885bd787a26402348e"}, {"156": "55848e0fcb8cce64a3da13885bd787a26402348e"}, {"157": "55848e0fcb8cce64a3da13885bd787a26402348e"}, {"158": "55848e0fcb8cce64a3da13885bd787a26402348e"}, {"159": "55848e0fcb8cce64a3da13885bd787a26402348e"}, {"160": "55848e0fcb8cce64a3da13885bd787a26402348e"}], "ctags": [{"_type": "tag", "name": "async_session_factory", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "pattern": "/^async_session_factory = async_sessionmaker($/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "db_session", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "pattern": "/^async def db_session() -> AsyncGenerator[AsyncSession, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncSession,None]", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "engine", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "pattern": "/^engine = create_async_engine($/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "get_db_connection", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "pattern": "/^async def get_db_connection() -> AsyncGenerator[AsyncConnection, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncConnection,None]", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "get_db_session", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "pattern": "/^async def get_db_session() -> AsyncGenerator[AsyncSession, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncSession,None]", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "init_db", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "pattern": "/^async def init_db() -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "logger", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "pattern": "/^logger = logging.getLogger(__name__)$/", "language": "Python", "kind": "variable"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/db/session.py", "hash": "4a06908bf6ded07ef4d9c5c59f8bcbf5", "format-version": 4, "code-base-name": "default", "fields": [{"name": "async_session_factory = async_sessionmaker(", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "engine = create_async_engine(", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "logger = logging.getLogger(__name__)", "scope": "", "scopeKind": "", "description": "unavailable"}]}