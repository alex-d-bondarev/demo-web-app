table "item" {
  schema = schema.im_db
  column "item_id" {
    null           = false
    type           = int
    auto_increment = true
  }
  column "name" {
    null = true
    type = varchar(255)
  }
  column "optimal_stock" {
    null = true
    type = int
  }
  column "volume" {
    null     = true
    type     = decimal(10,2)
    unsigned = false
  }
  column "weight" {
    null     = true
    type     = decimal(10,2)
    unsigned = false
  }
  primary_key {
    columns = [column.item_id]
  }
}
table "purchase_order" {
  schema = schema.im_db
  column "purchase_order_id" {
    null           = false
    type           = int
    auto_increment = true
  }
  column "created_dt" {
    null = true
    type = datetime
  }
  column "delivered_dt" {
    null = true
    type = datetime
  }
  column "status" {
    null = true
    type = varchar(255)
  }
  column "provider" {
    null = true
    type = varchar(255)
  }
  primary_key {
    columns = [column.purchase_order_id]
  }
}
table "purchase_order_item" {
  schema = schema.im_db
  column "purchase_order_item_id" {
    null           = false
    type           = int
    auto_increment = true
  }
  column "item_id" {
    null = true
    type = int
  }
  column "purchase_order_id" {
    null = true
    type = int
  }
  column "price" {
    null     = true
    type     = decimal(10,2)
    unsigned = false
  }
  column "quantity" {
    null = true
    type = int
  }
  primary_key {
    columns = [column.purchase_order_item_id]
  }
}
table "review" {
  schema = schema.im_db
  column "review_id" {
    null           = false
    type           = int
    auto_increment = true
  }
  column "start_dt" {
    null = true
    type = datetime
  }
  column "end_dt" {
    null = true
    type = datetime
  }
  column "status" {
    null = true
    type = varchar(255)
  }
  primary_key {
    columns = [column.review_id]
  }
}
table "review_item" {
  schema = schema.im_db
  column "review_item_id" {
    null           = false
    type           = int
    auto_increment = true
  }
  column "review_id" {
    null = true
    type = int
  }
  column "item_id" {
    null = true
    type = int
  }
  column "quantity" {
    null = true
    type = int
  }
  primary_key {
    columns = [column.review_item_id]
  }
}
schema "im_db" {
  charset = "utf8mb4"
  collate = "utf8mb4_0900_ai_ci"
}
