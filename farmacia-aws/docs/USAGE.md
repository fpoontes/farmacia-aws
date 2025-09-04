# Guia de Uso e Implantação (Detalhado)

## 1) Criar usuário/role e credenciais (se necessário)
- Configure o AWS CLI: `aws configure`
- Garanta permissões: S3, Lambda, API Gateway, IAM, DynamoDB, CloudWatch

## 2) Terraform — variáveis úteis
- Região: `-var="aws_region=us-east-1"` (pode trocar por `sa-east-1` — São Paulo)
- Ajuste nomes de recursos se tiver conflito de bucket (global).

## 3) Front-end (S3)
- Após `terraform apply`, rode `aws s3 sync ../../src/frontend s3://<BUCKET> --delete`
- Acesse `http://<website-endpoint>` retornado nos outputs
- Edite o `index.html` para apontar para sua `api_base_url` se quiser travar o domínio no código

## 4) API (Gateway + Lambda + DynamoDB)
- A API vem com CORS permissivo para facilitar testes didáticos
- Endpoints: `/products`, `/products/{id}`, `/orders`
- Dados iniciais de produtos são “seedados” diretamente no código da Lambda caso a tabela esteja vazia (id 1–3)

## 5) (Opcional) Cognito
- Crie um **User Pool** e um **App Client** (sem secret)
- Gere um JWT após login e configure a rota do API Gateway para exigir authorizer JWT
- No front-end, inclua o token no header `Authorization: Bearer <jwt>`

## 6) Logs e troubleshooting
- Verifique CloudWatch Logs: grupos `/aws/lambda/catalog_handler` e `/aws/lambda/order_handler`
- Em caso de erro de permissão, confira as IAM Policies geradas pelo Terraform

## 7) Destruir recursos
```bash
terraform destroy -auto-approve -var="aws_region=us-east-1"
```
