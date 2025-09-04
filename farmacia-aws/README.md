# Plataforma Virtual de Farmácia — AWS (DIO Bootcamp)

Este repositório contém um projeto *completo* e pronto para entrega no bootcamp da DIO, modelando uma **farmácia fictícia** chamada **Farmácia Vida+**. A solução é **serverless** e usa serviços gerenciados da AWS para entregar:
- **Front-end estático** (S3 com website hosting)
- **API** (API Gateway HTTP API v2 + AWS Lambda em Python)
- **Banco de dados** (DynamoDB)
- **Autenticação (opcional)** com Amazon Cognito (documentada em `docs/USAGE.md`)
- **Observabilidade** (CloudWatch Logs) e **CORS** habilitado
- Implantação via **Terraform** (IaC) + exemplo de CI/CD no GitHub Actions

> **Meta didática:** aplicar fundamentos de Cloud (IAM, API, Compute, Storage, NoSQL, Observabilidade) com *baixa fricção* para testes locais e na nuvem.

---

## Arquitetura

```mermaid
flowchart LR
    A[Usuário (Browser)] -->|HTTPS| CF[(API Gateway HTTP API)]
    A -->|HTTP (Site)| S3[S3 Static Website]
    CF -->|Invoke| L1[Lambda catalog_handler]
    CF -->|Invoke| L2[Lambda order_handler]
    L1 --> D1[(DynamoDB: Products)]
    L2 --> D2[(DynamoDB: Orders)]
    subgraph Observabilidade
      CW[(CloudWatch Logs)]
    end
    L1 --> CW
    L2 --> CW
```

### Serviços Utilizados
- **Amazon S3**: hospeda o front-end estático (`src/frontend/`).
- **Amazon API Gateway (HTTP API v2)**: expõe endpoints `/products` (GET) e `/orders` (POST).
- **AWS Lambda (Python 3.12)**: funções de catálogo e pedidos.
- **Amazon DynamoDB**: tabelas `Products` (PK `id`) e `Orders` (PK `id`).
- **Amazon CloudWatch**: logs de execução das Lambdas.
- **(Opcional)** Amazon Cognito: autenticação para rotas privadas (documentado).

---

## Endpoints (OpenAPI)
A especificação está em `docs/openapi.yaml`. Em produção, você terá algo como:
- `GET /products` → lista produtos
- `GET /products/{id}` → obtém um produto
- `POST /orders` → cria um pedido `{ productId, qty, customer }`

Exemplos de `curl` estão mais abaixo.

---

## Estrutura do Repositório

```
farmacia-aws/
├─ README.md
├─ relatorio-implementacao.md
├─ docs/
│  ├─ USAGE.md
│  └─ openapi.yaml
├─ infra/
│  └─ terraform/
│     ├─ provider.tf
│     ├─ variables.tf
│     ├─ main.tf
│     ├─ outputs.tf
│     └─ versions.tf
├─ src/
│  ├─ frontend/
│  │  └─ index.html
│  └─ lambda/
│     ├─ catalog_handler.py
│     └─ order_handler.py
├─ .github/
│  └─ workflows/
│     └─ terraform.yml
└─ .gitignore
```

---

## Pré-requisitos
- Conta AWS com permissões para S3, API Gateway, Lambda, IAM e DynamoDB
- **AWS CLI** configurado (`aws configure`)
- **Terraform** >= 1.5 instalado
- Python 3.12 (para rodar e empacotar Lambda localmente, caso queira)

---

## Deploy com Terraform (rápido)
1. Entre na pasta IaC:
   ```bash
   cd infra/terraform
   terraform init
   terraform plan -var="aws_region=us-east-1"
   terraform apply -auto-approve -var="aws_region=us-east-1"
   ```

2. Ao final, anote os **outputs**:
   - `api_base_url`
   - `site_bucket_website_endpoint`

3. Suba o front-end para o bucket de site:
   ```bash
   aws s3 sync ../../src/frontend s3://$(terraform output -raw site_bucket_name) --delete
   ```

4. Acesse o site pelo endpoint retornado e teste a API.

> **Dica:** Se aparecer erro de CORS ao chamar API pelo navegador, aguarde a propagação da configuração do API Gateway (normalmente 1–2 minutos) e recarregue a página.

---

## Testes rápidos de API

Após o `apply`, exporte a URL base:
```bash
export API="$(terraform -chdir=infra/terraform output -raw api_base_url)"
```

**Listar produtos**
```bash
curl -s "$API/products" | jq
```

**Buscar um produto**
```bash
curl -s "$API/products/1" | jq
```

**Criar um pedido**
```bash
curl -s -X POST "$API/orders"   -H "Content-Type: application/json"   -d '{"productId":"1","qty":2,"customer":"felipe@exemplo.com"}' | jq
```

---

## Custos (estimativa didática)
- DynamoDB (nível gratuito razoável), Lambda (pagamento por uso), API Gateway HTTP (baixo custo) e S3 (centavos por mês). Para uso de estudo, tende a ficar **próximo de zero**.
- **Importante:** após terminar, rode `terraform destroy` para evitar cobranças.

---

## Segurança e Boas Práticas
- Mínimo privilégio nas IAM Policies das Lambdas.
- CORS restrito (ajuste domínios em `main.tf` conforme seu front-end).
- Para produção, prefira **CloudFront** sobre website público do S3 e habilite **WAF**.
- Variáveis sensíveis em **AWS Systems Manager Parameter Store** ou **Secrets Manager**.

---

## Como apresentar no bootcamp
- Mostre o **README** (arquitetura, passos e comandos).
- Abra o **relatório** `relatorio-implementacao.md` (modelo solicitado na aula).
- Faça um **deploy ao vivo** de `terraform apply` e uma chamada `curl`.
- Demonstre o site estático listando os produtos.

---

## Licença
MIT — uso educacional e comercial permitido com atribuição.
