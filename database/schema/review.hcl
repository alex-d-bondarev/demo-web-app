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