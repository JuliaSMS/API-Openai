# Chatbot com OpenAI GPT-3.5

Este é um projeto simples para criar um chatbot utilizando o modelo GPT-3.5 da OpenAI. O script Python permite que os usuários façam perguntas ao chatbot e recebam respostas geradas pelo modelo. Além disso, há um mecanismo de moderação que verifica se as perguntas são seguras antes de enviá-las ao modelo.

## Pré-requisitos

- Python 3.6 ou superior
- Uma conta na OpenAI com acesso ao modelo GPT-3.5
- Chave de API da OpenAI

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/JuliaSMS/chatbot-openai.git
   cd chatbot-openai


## Explicações Adicionais
Configuração Inicial: O código começa importando os módulos necessários (os, openai, dotenv e colorama) e carrega a chave da API da OpenAI a partir do arquivo .env usando load_dotenv().

Função get_response: Esta função constrói uma lista de mensagens que inclui instruções, perguntas e respostas anteriores, e então usa openai.ChatCompletion.create para obter uma resposta do modelo GPT-3.5.

Função get_moderation: Verifica se uma pergunta é segura usando openai.Moderation.create, que chama o serviço de moderação da OpenAI para avaliar se a pergunta pode ser feita com segurança ao modelo.

Função main: Implementa um loop onde o usuário pode fazer perguntas ao bot. Verifica a moderação antes de enviar a pergunta ao modelo e exibe erros se houver. Armazena o histórico de perguntas e respostas e exibe a resposta do bot para o usuário.

Este código facilita a interação com o modelo de chatbot da OpenAI de forma segura e organizada, mantendo um histórico de conversas passadas.



Este README fornece uma visão geral clara do projeto, instruções passo a passo para configuração e uso, estrutura do projeto e informações sobre contribuições e licenciamento. Certifique-se de personalizar as seções conforme necessário para refletir os detalhes específicos do seu projeto.
