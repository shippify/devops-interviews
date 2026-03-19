# Use Case: Lambda não consegue listar S3 nem acessar API externa

## Configuração obrigatória (faça isso primeiro)
1. Faça um fork deste repositório.  
2. No seu fork, configure o seguinte secret no GitHub:  
   - `AWS_ROLE_ARN` (utilizado pelo GitHub OIDC para assumir uma role IAM na AWS)  
3. Envie seu usuário do GitHub para o entrevistador.  
   - O entrevistador irá conceder permissões temporárias e ajustar as condições de confiança do OIDC na AWS para permitir que seu repositório + branch assumam a role e façam o deploy.

---

## Como executar (somente via GitHub)
1. Crie ou acesse uma branch chamada `fixes` no seu fork (baseada na `master`).  
2. Faça as alterações necessárias na branch `fixes` e dê push para disparar o workflow.  
3. Após a execução do workflow (deploy com Terraform), teste a Lambda diretamente no console da AWS (não há execução automática via CI).

---

## O que você recebe
Você terá acesso a um repositório público no GitHub que executa um assessment utilizando GitHub Actions:

- O GitHub Actions realiza o deploy da infraestrutura AWS usando Terraform.  
- Também faz o build de uma **imagem de container** para uma função Lambda e a publica.  
- Além disso, será fornecido um usuário de AWS para que você possa testar e revisar os recursos diretamente no console da AWS.

⚠️ O repositório foi propositalmente configurado com erros.  
Seu objetivo é corrigir esses problemas para que a Lambda funcione corretamente ao ser testada no console da AWS.

---

## Problemas atuais (sintomas)
Ao testar a Lambda após o deploy, você pode encontrar um ou mais dos seguintes problemas:

- **Falha no CI/deploy antes do Terraform (OIDC)**  
  - O workflow falha na etapa de credenciais AWS porque o OIDC do GitHub não consegue assumir a role.  
  - É necessário corrigir as permissões do workflow.

- **Erros relacionados ao S3**  
  - Exemplo: `AccessDenied` ao listar buckets ou objetos.

- **Erros ao acessar API externa**  
  - Exemplo: timeout ou falha de conexão ao chamar um endpoint HTTPS.

- **Possíveis erros de container/runtime**  
  - Exemplo: problemas com handler ou importação de módulos.

---

## Sua tarefa
Seu envio é bem-sucedido quando:

- O workflow do GitHub Actions for corrigido e executado com sucesso
- Não houver erros de runtime ou na resposta da invocação da Lambda
---

## Onde procurar no repositório
- `.github/workflows`:
  - `terraform.yml` (workflow para o deploy na AWS)  

- `lambda/`:
  - `Dockerfile` (build da imagem do container da Lambda)  
  - `main.py` (código handler da Lambda)  

- `terraform/`:
  - Permissões IAM da role de execução da Lambda  
  - Configuração de VPC, subnets e rotas (impactam acesso à internet)

---

## Dicas
1. **Permissões do GitHub Actions (OIDC)**  
   Certifique-se de incluir as permissões corretas no workflow:
   ```yaml
   permissions:
     contents: read
     id-token: write
     ```
     Referência:
https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers

2.	**Erro de handler/import**
	- Verifique se a imagem do container está estruturada corretamente.
	- O handler precisa estar no caminho esperado pelo runtime da Lambda.
3.	**Erro AccessDenied no S3**
	- Revise as permissões da role IAM da Lambda conforme o que o código em lambda/main.py exige.
4.	**Timeout ao acessar API externa**
	- A Lambda está dentro de uma VPC.
	- Verifique se há saída para a internet (NAT Gateway ou configuração equivalente).
