variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}


variable "lambda_function_name"{
  description = "nome da função lambda"
  type        = string
}

variable "lambda_filename"{
  description = "nome do arquivo a ser zipado e upado"
  type        = string
}


variable "api_name"{
  description = "nome do api-gtw"
  type        = string
}

variable "route_key_cep"{
  description = "Rota da api GET CEP"
  type        = string

}

variable "logs_retention"{
  description = "Rota da api GET CEP"
  type        = number
  default     = 1
}