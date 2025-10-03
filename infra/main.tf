provider "aws" {
  region = "us-east-1"
}

# Role para Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Atrelando a policy básica
resource "aws_iam_role_policy_attachment" "attach_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Função Lambda
resource "aws_lambda_function" "user_api" {
  function_name = "user-api-func"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  filename      = "../lambda_function.zip"   # ex: ./build/lambda.zip
  source_code_hash = filebase64sha256("../lambda_function.zip")
}

# API Gateway
resource "aws_apigatewayv2_api" "api" {
  name          = "user-api"
  protocol_type = "HTTP"
}

# Integração Lambda ↔ API
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.user_api.invoke_arn
  payload_format_version = "2.0"
}

# Rota POST /login
resource "aws_apigatewayv2_route" "login_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /login"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Rota POST /cadastro
resource "aws_apigatewayv2_route" "cadastro_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /cadastro"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Permissão Lambda para ser chamada pelo API Gateway
resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.user_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}

# Stage default
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

# Logs no CloudWatch
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/user-api-func"
  retention_in_days = var.logs_retention
}
