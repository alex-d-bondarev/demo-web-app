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
