{"is_source_file": true, "format": "Python", "description": "This module defines Pydantic schemas for order and order item validation, including creation, updating, and reading of order data.", "external_files": ["app/models/order.py", "app/schemas/BaseCreateSchema.py", "app/schemas/BaseReadSchema.py", "app/schemas/BaseSchema.py", "app/schemas/BaseUpdateSchema.py"], "external_methods": [], "published": ["OrderCreate", "OrderUpdate", "OrderRead", "OrderItemCreate", "OrderItemUpdate", "OrderItemRead"], "classes": [{"name": "OrderItemBase", "description": "Base schema for order item data containing fields common to all order item schemas."}, {"name": "OrderItemCreate", "description": "Schema for creating a new order item, inherits from OrderItemBase."}, {"name": "OrderItemUpdate", "description": "Schema for updating an existing order item, all fields are optional."}, {"name": "OrderItemRead", "description": "Schema for reading order item data, inherits from OrderItemBase."}, {"name": "OrderBase", "description": "Base schema for order data containing fields common to all order schemas."}, {"name": "OrderCreate", "description": "Schema for creating a new order, inherits from OrderBase and adds items field."}, {"name": "OrderUpdate", "description": "Schema for updating an existing order, all fields are optional."}, {"name": "OrderRead", "description": "Schema for reading order data, inherits from OrderBase and adds items field."}], "methods": [{"name": "Optional[Decimal] validate_price(cls, v: Optional[Decimal])", "description": "Validates that the price has at most 2 decimal places.", "scope": "OrderItemBase", "scopeKind": "class"}, {"name": "Decimal validate_total_amount(cls, v: Decimal)", "description": "Validates that total amount has at most 2 decimal places.", "scope": "OrderBase", "scopeKind": "class"}], "calls": [], "search-terms": ["Pydantic", "Order", "OrderItem", "validation"], "state": 2, "file_id": 20, "knowledge_revision": 45, "git_revision": "", "ctags": [{"_type": "tag", "name": "OrderBase", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderBase(BaseSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "OrderCreate", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderCreate(OrderBase, BaseCreateSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "OrderItemBase", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderItemBase(BaseSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "OrderItemCreate", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderItemCreate(OrderItemBase, BaseCreateSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "OrderItemRead", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderItemRead(OrderItemBase, BaseReadSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "OrderItemUpdate", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderItemUpdate(BaseUpdateSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "OrderRead", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderRead(OrderBase, BaseReadSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "OrderUpdate", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^class OrderUpdate(BaseUpdateSchema):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "customer_email", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    customer_email: EmailStr = Field($/", "language": "Python", "typeref": "typename:EmailStr", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "customer_email", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    customer_email: Optional[EmailStr] = Field($/", "language": "Python", "typeref": "typename:Optional[EmailStr]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "customer_id", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    customer_id: Optional[int] = Field($/", "language": "Python", "typeref": "typename:Optional[int]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "customer_name", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    customer_name: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "customer_name", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    customer_name: str = Field($/", "language": "Python", "typeref": "typename:str", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "items", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    items: List[OrderItemCreate] = Field($/", "language": "Python", "typeref": "typename:List[OrderItemCreate]", "kind": "variable", "scope": "OrderCreate", "scopeKind": "class"}, {"_type": "tag", "name": "items", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    items: List[OrderItemRead] = Field($/", "language": "Python", "typeref": "typename:List[OrderItemRead]", "kind": "variable", "scope": "OrderRead", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    model_config = {$/", "language": "Python", "kind": "variable", "scope": "OrderCreate", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    model_config = {$/", "language": "Python", "kind": "variable", "scope": "OrderItemCreate", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    model_config = {$/", "language": "Python", "kind": "variable", "scope": "OrderItemRead", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    model_config = {$/", "language": "Python", "kind": "variable", "scope": "OrderItemUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    model_config = {$/", "language": "Python", "kind": "variable", "scope": "OrderRead", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    model_config = {$/", "language": "Python", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "notes", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    notes: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "notes", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    notes: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "order_id", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    order_id: int = Field(..., description=\"Order ID\")$/", "language": "Python", "typeref": "typename:int", "kind": "variable", "scope": "OrderItemRead", "scopeKind": "class"}, {"_type": "tag", "name": "payment_id", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    payment_id: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "payment_id", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    payment_id: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "payment_method", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    payment_method: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "payment_method", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    payment_method: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "price_at_purchase", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    price_at_purchase: Optional[Decimal] = Field($/", "language": "Python", "typeref": "typename:Optional[Decimal]", "kind": "variable", "scope": "OrderItemBase", "scopeKind": "class"}, {"_type": "tag", "name": "product_id", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    product_id: int = Field($/", "language": "Python", "typeref": "typename:int", "kind": "variable", "scope": "OrderItemBase", "scopeKind": "class"}, {"_type": "tag", "name": "product_name", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    product_name: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderItemBase", "scopeKind": "class"}, {"_type": "tag", "name": "product_sku", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    product_sku: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderItemBase", "scopeKind": "class"}, {"_type": "tag", "name": "quantity", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    quantity: Optional[int] = Field($/", "language": "Python", "typeref": "typename:Optional[int]", "kind": "variable", "scope": "OrderItemUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "quantity", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    quantity: int = Field($/", "language": "Python", "typeref": "typename:int", "kind": "variable", "scope": "OrderItemBase", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_address", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_address: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_address", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_address: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_city", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_city: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_city", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_city: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_country", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_country: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_country", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_country: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_postal_code", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_postal_code: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "shipping_postal_code", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    shipping_postal_code: Optional[str] = Field($/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "status", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    status: Optional[OrderStatus] = Field($/", "language": "Python", "typeref": "typename:Optional[OrderStatus]", "kind": "variable", "scope": "OrderUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "status", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    status: OrderStatus = Field($/", "language": "Python", "typeref": "typename:OrderStatus", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "total_amount", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    total_amount: Decimal = Field($/", "language": "Python", "typeref": "typename:Decimal", "kind": "variable", "scope": "OrderBase", "scopeKind": "class"}, {"_type": "tag", "name": "validate_price", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    def validate_price(cls, v: Optional[Decimal]) -> Optional[Decimal]:$/", "language": "Python", "typeref": "typename:Optional[Decimal]", "kind": "member", "signature": "(cls, v: Optional[Decimal])", "scope": "OrderItemBase", "scopeKind": "class"}, {"_type": "tag", "name": "validate_total_amount", "path": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "pattern": "/^    def validate_total_amount(cls, v: Decimal) -> Decimal:$/", "language": "Python", "typeref": "typename:Decimal", "kind": "member", "signature": "(cls, v: Decimal)", "scope": "OrderBase", "scopeKind": "class"}], "filename": "/home/kavia/workspace/API-Performance-Optimization-L.0.8/app/schemas/order.py", "hash": "ef299e9f9e621e1a5efd619ab53aadac", "format-version": 4, "code-base-name": "default", "fields": [{"name": "EmailStr customer_email", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[EmailStr] customer_email", "scope": "OrderUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[int] customer_id", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] customer_name", "scope": "OrderUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "str customer_name", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "List[OrderItemCreate] items", "scope": "OrderCreate", "scopeKind": "class", "description": "unavailable"}, {"name": "List[OrderItemRead] items", "scope": "OrderRead", "scopeKind": "class", "description": "unavailable"}, {"name": "model_config = {", "scope": "OrderCreate", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] notes", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "int order_id", "scope": "OrderItemRead", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] payment_id", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] payment_method", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[Decimal] price_at_purchase", "scope": "OrderItemBase", "scopeKind": "class", "description": "unavailable"}, {"name": "int product_id", "scope": "OrderItemBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] product_name", "scope": "OrderItemBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] product_sku", "scope": "OrderItemBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[int] quantity", "scope": "OrderItemUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "int quantity", "scope": "OrderItemBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] shipping_address", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] shipping_city", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] shipping_country", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] shipping_postal_code", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[OrderStatus] status", "scope": "OrderUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "OrderStatus status", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Decimal total_amount", "scope": "OrderBase", "scopeKind": "class", "description": "unavailable"}], "revision_history": [{"45": ""}]}