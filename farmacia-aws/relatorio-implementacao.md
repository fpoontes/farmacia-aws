# RELATÓRIO DE IMPLEMENTAÇÃO DE SERVIÇOS AWS

Data: 04/09/2025
Empresa: Farmácia Vida+
Responsável: Felipe Elias de Pontes

## Introdução
Este relatório apresenta o processo de implementação de serviços AWS para a plataforma virtual da **Farmácia Vida+**, realizado por **Felipe Elias de Pontes**. O objetivo do projeto foi **projetar e implantar** três serviços AWS principais para suportar um site de catálogo e uma API de pedidos, visando **baixa latência**, **baixo custo** e **alta disponibilidade**.

## Descrição do Projeto
O projeto foi dividido em 3 etapas, cada uma com seus objetivos específicos. A seguir, as etapas do projeto:

**Etapa 1**
- **Nome da ferramenta:** Amazon S3 (Static Website Hosting)
- **Foco da ferramenta:** Hospedar o front-end estático da farmácia
- **Descrição de caso de uso:** Entregar um `index.html` público com lista de produtos e integração via JavaScript com a API.

**Etapa 2**
- **Nome da ferramenta:** API Gateway (HTTP API v2) + AWS Lambda + DynamoDB
- **Foco da ferramenta:** Expor endpoints REST para catálogo e criação de pedidos
- **Descrição de caso de uso:** `GET /products` e `GET /products/{id}` consultando a tabela **Products** no DynamoDB; `POST /orders` criando registros na tabela **Orders**.

**Etapa 3**
- **Nome da ferramenta:** CloudWatch Logs (+ Cognito opcional)
- **Foco da ferramenta:** Observabilidade e opção de autenticação futura
- **Descrição de caso de uso:** Centralizar logs das Lambdas em CloudWatch para auditoria e troubleshooting. Caso necessário, proteger rotas com **Cognito User Pool** (documentado em `docs/USAGE.md`).

## Conclusão
A implementação na **Farmácia Vida+** atingiu os objetivos esperados: **entrega rápida**, **redução de custos** ao adotar serverless, e **escalabilidade automática**. Recomenda-se manter a monitoração via CloudWatch, versionar a infraestrutura com Terraform e, em evolução futura, adicionar **CloudFront + WAF**.

## Anexos
- `docs/openapi.yaml` — especificação da API
- `docs/USAGE.md` — passos detalhados de uso e variações (Cognito)
- `infra/terraform/*.tf` — infraestrutura como código
- `src/lambda/*.py` — funções Lambda
- `src/frontend/index.html` — site estático
- `.github/workflows/terraform.yml` — CI/CD (exemplo)

---
Assinatura do Responsável pelo Projeto:

**Felipe Elias de Pontes**
