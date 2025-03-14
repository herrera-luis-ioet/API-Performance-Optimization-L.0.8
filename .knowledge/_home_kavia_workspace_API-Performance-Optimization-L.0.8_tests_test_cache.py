{"is_source_file": true, "format": "Python", "description": "Contains tests for Redis cache functionality, including serialization and deserialization of SQLAlchemy models, specifically for Product objects.", "external_files": ["app.core.cache.RedisCache", "app.core.cache.generate_cache_key", "app.core.cache.CustomJSONEncoder", "app.models.product.Product"], "external_methods": ["app.core.cache.RedisCache.set", "app.core.cache.RedisCache.get", "json.loads", "json.dumps"], "published": ["test_product_serialization", "test_generate_cache_key_with_product", "test_cache_get_with_product", "test_decimal_field_serialization", "test_decimal_edge_cases_serialization", "test_custom_json_encoder_with_decimal"], "classes": [], "methods": [{"name": "mock_redis_client()", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "redis_cache(mock_redis_client)", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "sample_product()", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "test_cache_get_with_product(redis_cache, sample_product, mock_redis_client)", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "test_custom_json_encoder_with_decimal()", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "test_decimal_edge_cases_serialization(redis_cache, mock_redis_client)", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "test_decimal_field_serialization(redis_cache, mock_redis_client)", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "test_generate_cache_key_with_product(sample_product)", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "test_product_serialization(redis_cache, sample_product, mock_redis_client)", "scope": "", "scopeKind": "", "description": "unavailable"}], "calls": ["app.core.cache.RedisCache.set", "app.core.cache.RedisCache.get", "json.loads", "json.dumps"], "search-terms": ["RedisCache", "Product", "serialization", "deserialization", "custom JSON encoder"], "state": 2, "file_id": 47, "knowledge_revision": 231, "git_revision": "d7592a034b97c1d7f4d4a83854b7b38577ce17e3", "revision_history": [{"226": "d7592a034b97c1d7f4d4a83854b7b38577ce17e3"}, {"231": "d7592a034b97c1d7f4d4a83854b7b38577ce17e3"}], "ctags": [{"_type": "tag", "name": "mock_redis_client", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^def mock_redis_client():$/", "language": "Python", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "redis_cache", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^def redis_cache(mock_redis_client):$/", "language": "Python", "kind": "function", "signature": "(mock_redis_client)"}, {"_type": "tag", "name": "sample_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^def sample_product():$/", "language": "Python", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "test_cache_get_with_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^async def test_cache_get_with_product(redis_cache, sample_product, mock_redis_client):$/", "language": "Python", "kind": "function", "signature": "(redis_cache, sample_product, mock_redis_client)"}, {"_type": "tag", "name": "test_custom_json_encoder_with_decimal", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^def test_custom_json_encoder_with_decimal():$/", "language": "Python", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "test_decimal_edge_cases_serialization", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^async def test_decimal_edge_cases_serialization(redis_cache, mock_redis_client):$/", "language": "Python", "kind": "function", "signature": "(redis_cache, mock_redis_client)"}, {"_type": "tag", "name": "test_decimal_field_serialization", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^async def test_decimal_field_serialization(redis_cache, mock_redis_client):$/", "language": "Python", "kind": "function", "signature": "(redis_cache, mock_redis_client)"}, {"_type": "tag", "name": "test_generate_cache_key_with_product", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^async def test_generate_cache_key_with_product(sample_product):$/", "language": "Python", "kind": "function", "signature": "(sample_product)"}, {"_type": "tag", "name": "test_product_serialization", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "pattern": "/^async def test_product_serialization(redis_cache, sample_product, mock_redis_client):$/", "language": "Python", "kind": "function", "signature": "(redis_cache, sample_product, mock_redis_client)"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/tests/test_cache.py", "hash": "ff3e9daffa554b5450e18543e97f18e7", "format-version": 4, "code-base-name": "default"}