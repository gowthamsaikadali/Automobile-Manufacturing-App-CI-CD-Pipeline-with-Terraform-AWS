terraform {
  backend "s3" {
    bucket         = "automobiletfstate2026"
    key            = "prod/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "automobiletflock"
    encrypt        = true
  }
}
