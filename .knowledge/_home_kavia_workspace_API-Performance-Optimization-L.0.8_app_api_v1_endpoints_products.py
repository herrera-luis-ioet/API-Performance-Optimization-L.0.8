{"is_source_file": true, "format": "Python", "description": "API endpoints module for product operations, defining various routes for CRUD operations and product retrieval with pagination.", "external_files": ["app/api/deps", "app/core/cache", "app/crud/product", "app/schemas/product"], "external_methods": ["app.api.deps.get_db", "app.api.deps.get_pagination_params", "app.api.deps.handle_db_exceptions", "app.api.deps.rate_limit", "app.crud.product.get_multi", "app.crud.product.get_active", "app.crud.product.get_by_category", "app.crud.product.get_by_sku", "app.crud.product.get", "app.crud.product.create", "app.crud.product.update", "app.crud.product.update_stock", "app.crud.product.remove"], "published": ["router"], "classes": [], "methods": [{"name": "Any get_products( request: Request, db: AsyncSession = Depends(get_db), pagination: dict = Depends(get_pagination_params) )", "description": "Retrieves a paginated list of all products.", "scope": "", "scopeKind": ""}, {"name": "Any get_active_products( request: Request, db: AsyncSession = Depends(get_db), pagination: dict = Depends(get_pagination_params) )", "description": "Retrieves a paginated list of active products.", "scope": "", "scopeKind": ""}, {"name": "Any get_products_by_category( request: Request, category: str = Path(..., description=\"Product category\"), db: AsyncSession = Depends(get_db), pagination: dict = Depends(get_pagination_params) )", "description": "Retrieves a paginated list of products filtered by a specific category.", "scope": "", "scopeKind": ""}, {"name": "Any get_product_by_sku( request: Request, sku: str = Path(..., description=\"Product SKU\"), db: AsyncSession = Depends(get_db) )", "description": "Retrieves a specific product using its SKU, or raises a 404 if not found.", "scope": "", "scopeKind": ""}, {"name": "Any get_product( request: Request, product_id: int = Path(..., description=\"Product ID\"), db: AsyncSession = Depends(get_db) )", "description": "Retrieves a specific product using its ID, or raises a 404 if not found.", "scope": "", "scopeKind": ""}, {"name": "Any create_product( product_in: ProductCreate, db: AsyncSession = Depends(get_db) )", "description": "Creates a new product based on the provided data.", "scope": "", "scopeKind": ""}, {"name": "Any update_product( product_in: ProductUpdate, product_id: int = Path(..., description=\"Product ID\"), db: AsyncSession = Depends(get_db) )", "description": "Updates an existing product using its ID.", "scope": "", "scopeKind": ""}, {"name": "Any update_product_stock( product_id: int = Path(..., description=\"Product ID\"), quantity_change: int = Query(..., description=\"Change in stock quantity (positive for increase, negative for decrease)\"), db: AsyncSession = Depends(get_db) )", "description": "Updates the stock quantity of a specific product.", "scope": "", "scopeKind": ""}, {"name": "None delete_product( product_id: int = Path(..., description=\"Product ID\"), db: AsyncSession = Depends(get_db) )", "description": "Deletes a specific product using its ID.", "scope": "", "scopeKind": ""}], "calls": ["get_db", "get_pagination_params", "handle_db_exceptions", "rate_limit", "product.get_multi", "product.get_active", "product.get_by_category", "product.get_by_sku", "product.get", "product.create", "product.update", "product.update_stock", "product.remove"], "search-terms": ["product endpoints", "API product operations", "get products", "create product"], "state": 2, "file_id": 26, "knowledge_revision": 218, "git_revision": "02793a05313a28a79b82fd7e0ce05f76605060ca", "revision_history": [{"58": ""}, {"70": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"71": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"72": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"73": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"74": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"75": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"76": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"77": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"78": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"79": "0984669f42e62abb834a1a125ba6194fb82914c5"}, {"128": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"129": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"130": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"131": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"132": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"133": "3ca38c1a5bb82a63be25191740c83663bd590a04"}, {"154": "a15e52cdf83686d94b96d45a1957085ae53f782e"}, {"162": "a15e52cdf83686d94b96d45a1957085ae53f782e"}, {"218": "02793a05313a28a79b82fd7e0ce05f76605060ca"}], "ctags": [{"_type": "tag", "name": "create_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def create_product($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( product_in: ProductCreate, db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "delete_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def delete_product($/", "language": "Python", "typeref": "typename:None", "kind": "function", "signature": "( product_id: int = Path(..., description=\"Product ID\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "get_active_products", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def get_active_products($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( request: Request, db: AsyncSession = Depends(get_db), pagination: dict = Depends(get_pagination_params) )"}, {"_type": "tag", "name": "get_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def get_product($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( request: Request, product_id: int = Path(..., description=\"Product ID\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "get_product_by_sku", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def get_product_by_sku($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( request: Request, sku: str = Path(..., description=\"Product SKU\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "get_products", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def get_products($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( request: Request, db: AsyncSession = Depends(get_db), pagination: dict = Depends(get_pagination_params) )"}, {"_type": "tag", "name": "get_products_by_category", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def get_products_by_category($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( request: Request, category: str = Path(..., description=\"Product category\"), db: AsyncSession = Depends(get_db), pagination: dict = Depends(get_pagination_params) )"}, {"_type": "tag", "name": "router", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^router = APIRouter()$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "update_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def update_product($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( product_in: ProductUpdate, product_id: int = Path(..., description=\"Product ID\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "update_product_stock", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "pattern": "/^async def update_product_stock($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( product_id: int = Path(..., description=\"Product ID\"), quantity_change: int = Query(..., description=\"Change in stock quantity (positive for increase, negative for decrease)\"), db: AsyncSession = Depends(get_db) )"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/api/v1/endpoints/products.py", "hash": "ab671b7cc1c58dea3bc4a8a8b16fb272", "format-version": 4, "code-base-name": "default", "fields": [{"name": "router = APIRouter()", "scope": "", "scopeKind": "", "description": "unavailable"}]}