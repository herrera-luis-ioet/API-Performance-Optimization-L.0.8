{"is_source_file": true, "format": "Python", "description": "This file contains test fixtures for database and API testing, specifically for the API Performance Optimization project. It provides various fixtures for setting up test environments, including test database connections and a FastAPI application instance.", "external_files": ["app.api.deps", "app.core.config", "app.db.base", "app.models.product", "app.models.order", "app.main"], "external_methods": ["app.api.deps.get_db", "app.main.create_application"], "published": ["event_loop", "test_engine", "db_session", "app", "client", "test_products", "test_orders"], "classes": [{"name": "Product", "description": "Represents a product in the inventory system."}, {"name": "Order", "description": "Represents an order placed by a customer."}, {"name": "OrderItem", "description": "Represents an item in an order."}, {"name": "OrderStatus", "description": "Enumerates the various statuses an order can have."}], "methods": [{"name": "Generator event_loop()", "description": "Creates an event loop for tests.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncEngine,None] test_engine()", "description": "Creates a test database engine.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncSession,None] db_session(test_engine: AsyncEngine)", "description": "Creates a test database session.", "scope": "", "scopeKind": ""}, {"name": "FastAPI app(db_session: AsyncSession)", "description": "Creates a test FastAPI application.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncClient,None] client(app: FastAPI)", "description": "Creates a test client for the FastAPI application.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[list,None] test_products(db_session: AsyncSession)", "description": "Creates test products for use in tests.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[list,None] test_orders(db_session: AsyncSession, test_products: list)", "description": "Creates test orders for use in tests.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncSession,None] override_get_db()", "scope": "app", "scopeKind": "function", "description": "unavailable"}], "calls": ["asyncio.get_event_loop_policy().new_event_loop", "create_async_engine", "Base.metadata.drop_all", "Base.metadata.create_all", "await conn.run_sync(lambda sync_conn: inspector.get_table_names())", "await db_session.add(product)", "await db_session.commit()", "await db_session.refresh(product)", "await db_session.connect()", "await transaction.rollback()", "await session.close()", "await connection.close()"], "search-terms": ["test fixtures", "database testing", "API testing", "FastAPI application"], "state": 2, "file_id": 37, "knowledge_revision": 199, "git_revision": "623d4693516a9c0249316895de6c52edad714060", "revision_history": [{"95": ""}, {"100": ""}, {"101": ""}, {"107": "2112e7b6e9c1da1c187ac87f2e5669af04e38ead"}, {"109": "2112e7b6e9c1da1c187ac87f2e5669af04e38ead"}, {"110": "2112e7b6e9c1da1c187ac87f2e5669af04e38ead"}, {"113": "df757bb51613bac28bf49c666e1993d0585bbf2e"}, {"114": "df757bb51613bac28bf49c666e1993d0585bbf2e"}, {"121": "df757bb51613bac28bf49c666e1993d0585bbf2e"}, {"123": "df757bb51613bac28bf49c666e1993d0585bbf2e"}, {"127": "db26009eb51c1d1e59dfe8e186759e95d4f68e57"}, {"169": "a15e52cdf83686d94b96d45a1957085ae53f782e"}, {"196": "233aed965db0f003e7956bc5d812b279ad6b9f26"}, {"197": "623d4693516a9c0249316895de6c52edad714060"}, {"199": "623d4693516a9c0249316895de6c52edad714060"}], "ctags": [{"_type": "tag", "name": "app", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^async def app(db_session: AsyncSession) -> FastAPI:$/", "language": "Python", "typeref": "typename:FastAPI", "kind": "function", "signature": "(db_session: AsyncSession)"}, {"_type": "tag", "name": "client", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncClient,None]", "kind": "function", "signature": "(app: FastAPI)"}, {"_type": "tag", "name": "db_session", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncSession,None]", "kind": "function", "signature": "(test_engine: AsyncEngine)"}, {"_type": "tag", "name": "event_loop", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^def event_loop() -> Generator:$/", "language": "Python", "typeref": "typename:Generator", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "override_get_db", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:$/", "file": true, "language": "Python", "typeref": "typename:AsyncGenerator[AsyncSession,None]", "kind": "function", "signature": "()", "scope": "app", "scopeKind": "function"}, {"_type": "tag", "name": "test_engine", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^async def test_engine() -> AsyncGenerator[AsyncEngine, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncEngine,None]", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "test_orders", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^async def test_orders(db_session: AsyncSession, test_products: list) -> AsyncGenerator[list, Non/", "language": "Python", "typeref": "typename:AsyncGenerator[list,None]", "kind": "function", "signature": "(db_session: AsyncSession, test_products: list)"}, {"_type": "tag", "name": "test_products", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "pattern": "/^async def test_products(db_session: AsyncSession) -> AsyncGenerator[list, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[list,None]", "kind": "function", "signature": "(db_session: AsyncSession)"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/conftest.py", "hash": "3c6b86708a7ca4c2ba9e21d9bf2f96c6", "format-version": 4, "code-base-name": "default"}