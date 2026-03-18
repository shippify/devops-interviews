# Caso de uso (Candidato): A Lambda não consegue listar o S3 e não consegue acessar a API externa

## Configuração obrigatória (faça antes)
1. Faça um fork deste repositório.
2. No seu fork, defina o secret do repositório:
   - `AWS_ROLE_ARN` (usado pelo GitHub OIDC para assumir uma role de IAM na AWS)
3. Envie seu usuário do GitHub ao entrevistador. O entrevistador vai adicionar permissões temporárias / atualizar as condições de trust do OIDC para que seu repositório do GitHub + branch consigam assumir a role e fazer o deploy.

## Como executar (somente via GitHub)
1. Crie/checkout uma branch chamada `fixes` no seu fork (criada a partir de `master`).
2. Faça as alterações na branch `fixes` e dê push em `fixes` para disparar o workflow.
3. Depois que o workflow terminar (deploy via Terraform), teste a Lambda diretamente no AWS Console (não há invoke automático no CI).

## O que você recebe
Você terá um repositório público no GitHub que executa um assessment via GitHub Actions:

- O GitHub Actions faz deploy da infraestrutura na AWS com Terraform.
- Ele cria uma **imagem de container** para uma função Lambda e faz o deploy.

O repositório está **intencionalmente quebrado**. Seu trabalho é corrigir os problemas para que a Lambda funcione corretamente quando você testar no AWS Console.

## O que está falhando (sintomas atuais)
Quando você testar a Lambda (após o deploy), espere um ou mais destes problemas:

- **Falha no CI/deploy antes de o Terraform rodar (OIDC)**:
  a execução falha na etapa de credenciais porque o GitHub OIDC não consegue assumir a role da AWS. Corrija as permissões do workflow para o OIDC funcionar.
- **Erros relacionados ao S3** (por exemplo, `AccessDenied` ao listar buckets ou ao listar objetos dentro de um bucket).
- **Erros da API externa** (por exemplo, timeouts / falhas de conexão ao acessar um endpoint HTTPS).
- Possivelmente, **erros de container/runtime** (por exemplo, problemas de handler/módulo).

## Sua tarefa
Faça as mudanças necessárias para que, depois do seu commit e novo deploy:

1. A invocação da Lambda seja bem-sucedida.

## Onde olhar no repositório
- `lambda/`:
  - `Dockerfile` (build do container da Lambda)
  - `main.py` (código do handler da Lambda)
- `terraform/`:
  - IAM para a role de execução da Lambda
  - VPC/subnets/roteamento que afetam o egress da Lambda

## Dicas (sem entregar a solução completa)
1. **Se você receber erro de handler/módulo**
   - A imagem do container provavelmente não está colocando o handler no local esperado pelo runtime da Lambda.
2. **Se você ver `AccessDenied` no S3**
   - Verifique as permissões da role de execução da Lambda necessárias pelo código em `lambda/main.py`.
3. **Se você vir timeouts ao chamar uma URL HTTPS externa**
   - A Lambda roda dentro de subnets da VPC; confirme que ela tem acesso de saída para a internet via HTTPS.

## Critério de sucesso (Definition of Done)
Seu envio é bem-sucedido quando, no teste da Lambda no AWS Console:
- a Lambda retorna uma resposta sem erros de runtime/import,
- e o payload JSON mostra sucesso na listagem do S3 + na chamada da API externa.