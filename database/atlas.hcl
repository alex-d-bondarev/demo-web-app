env "local" {
  url = getenv("DB_URL")
  dev = getenv("DEV_DB")
  schema {
    src = "file://schema/"
  }
}
