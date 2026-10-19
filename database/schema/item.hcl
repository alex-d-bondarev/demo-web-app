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
