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
