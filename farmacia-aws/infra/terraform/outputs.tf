output "api_base_url" {
  description = "HTTP API base URL"
  value       = aws_apigatewayv2_api.api.api_endpoint
}

output "site_bucket_name" {
  description = "S3 bucket name for static website"
  value       = aws_s3_bucket.site.bucket
}

output "site_bucket_website_endpoint" {
  description = "S3 website endpoint"
  value       = aws_s3_bucket_website_configuration.site.website_endpoint
}
