{"is_source_file": true, "format": "Python", "description": "Tests for product API endpoints including functions to test getting, creating, updating, and deleting products.", "external_files": ["app/core/config.py", "app/models/product.py"], "external_methods": ["app.core.config.settings", "app.models.product.Product"], "published": [], "classes": [], "methods": [{"name": "test_get_products(client: AsyncClient, test_products: list)", "description": "Test getting all products.", "scope": "", "scopeKind": ""}, {"name": "test_get_active_products(client: AsyncClient, test_products: list)", "description": "Test getting active products.", "scope": "", "scopeKind": ""}, {"name": "test_get_products_by_category(client: AsyncClient, test_products: list)", "description": "Test getting products by category.", "scope": "", "scopeKind": ""}, {"name": "test_get_product_by_sku(client: AsyncClient, test_products: list)", "description": "Test getting a product by SKU.", "scope": "", "scopeKind": ""}, {"name": "test_get_product_by_sku_not_found(client: AsyncClient)", "description": "Test getting a product by SKU that doesn't exist.", "scope": "", "scopeKind": ""}, {"name": "test_get_product_by_id(client: AsyncClient, test_products: list)", "description": "Test getting a product by ID.", "scope": "", "scopeKind": ""}, {"name": "test_get_product_by_id_not_found(client: AsyncClient)", "description": "Test getting a product by ID that doesn't exist.", "scope": "", "scopeKind": ""}, {"name": "test_create_product(client: AsyncClient)", "description": "Test creating a new product.", "scope": "", "scopeKind": ""}, {"name": "test_create_product_duplicate_sku(client: AsyncClient, test_products: list)", "description": "Test creating a product with a duplicate SKU.", "scope": "", "scopeKind": ""}, {"name": "test_update_product(client: AsyncClient, test_products: list)", "description": "Test updating a product.", "scope": "", "scopeKind": ""}, {"name": "test_update_product_not_found(client: AsyncClient)", "description": "Test updating a product that doesn't exist.", "scope": "", "scopeKind": ""}, {"name": "test_update_product_stock(client: AsyncClient, test_products: list)", "description": "Test updating a product's stock quantity.", "scope": "", "scopeKind": ""}, {"name": "test_update_product_stock_negative(client: AsyncClient, test_products: list)", "description": "Test decreasing a product's stock quantity.", "scope": "", "scopeKind": ""}, {"name": "test_delete_product(client: AsyncClient, test_products: list, db_session: AsyncSession)", "description": "Test deleting a product.", "scope": "", "scopeKind": ""}, {"name": "test_delete_product_not_found(client: AsyncClient)", "description": "Test deleting a product that doesn't exist.", "scope": "", "scopeKind": ""}], "calls": ["client.get", "client.post", "client.put", "client.patch", "client.delete"], "search-terms": ["product", "API", "endpoint", "testing"], "state": 2, "file_id": 38, "knowledge_revision": 97, "git_revision": "", "ctags": [{"_type": "tag", "name": "test_create_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_create_product(client: AsyncClient):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient)"}, {"_type": "tag", "name": "test_create_product_duplicate_sku", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_create_product_duplicate_sku(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_delete_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_delete_product(client: AsyncClient, test_products: list, db_session: AsyncSession/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list, db_session: AsyncSession)"}, {"_type": "tag", "name": "test_delete_product_not_found", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_delete_product_not_found(client: AsyncClient):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient)"}, {"_type": "tag", "name": "test_get_active_products", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_get_active_products(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_get_product_by_id", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_get_product_by_id(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_get_product_by_id_not_found", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_get_product_by_id_not_found(client: AsyncClient):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient)"}, {"_type": "tag", "name": "test_get_product_by_sku", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_get_product_by_sku(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_get_product_by_sku_not_found", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_get_product_by_sku_not_found(client: AsyncClient):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient)"}, {"_type": "tag", "name": "test_get_products", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_get_products(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_get_products_by_category", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_get_products_by_category(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_update_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_update_product(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_update_product_not_found", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_update_product_not_found(client: AsyncClient):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient)"}, {"_type": "tag", "name": "test_update_product_stock", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_update_product_stock(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}, {"_type": "tag", "name": "test_update_product_stock_negative", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "pattern": "/^async def test_update_product_stock_negative(client: AsyncClient, test_products: list):$/", "language": "Python", "kind": "function", "signature": "(client: AsyncClient, test_products: list)"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/api/test_products.py", "hash": "dd6caff79c7500731db162fcefe481e8", "format-version": 4, "code-base-name": "default", "revision_history": [{"97": ""}]}