import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Style

# Carrega as variáveis de ambiente do arquivo .env, se existir
load_dotenv()

# Configura a chave da API da OpenAI a partir das variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Instruções para o bot
INSTRUCTIONS = """<<INSIRA AS INSTRUÇÕES AQUI>>"""

# Parâmetros para a interação com o modelo
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10  # Limite de quantas perguntas incluir no contexto

def get_response(instructions, previous_questions_and_answers, new_question):
    """Obtém uma resposta do ChatCompletion

    Args:
        instructions: As instruções para o bot de chat - determina como ele irá se comportar
        previous_questions_and_answers: Histórico do chat
        new_question: A nova pergunta para fazer ao bot

    Returns:
        O texto da resposta
    """
    # Constrói as mensagens
    messages = [
        { "role": "system", "content": instructions },
    ]
    # Adiciona as perguntas e respostas anteriores
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # Adiciona a nova pergunta
    messages.append({ "role": "user", "content": new_question })

    # Chama o ChatCompletion da OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Verifica se a pergunta é segura para perguntar ao modelo

    Parâmetros:
        question (str): A pergunta para verificar

    Retorna uma lista de erros se a pergunta não for segura, caso contrário, retorna None
    """

    # Dicionário de erros
    errors = {
        "hate": "Conteúdo que expressa, incita ou promove ódio com base em raça, gênero, etnia, religião, nacionalidade, orientação sexual, status de deficiência ou casta.",
        "hate/threatening": "Conteúdo odioso que também inclui violência ou dano sério ao grupo alvo.",
        "self-harm": "Conteúdo que promove, incentiva ou retrata atos de automutilação, como suicídio, cortes e distúrbios alimentares.",
        "sexual": "Conteúdo destinado a excitar sexualmente, como a descrição de atividade sexual, ou que promove serviços sexuais (excluindo educação sexual e bem-estar).",
        "sexual/minors": "Conteúdo sexual que inclui um indivíduo com menos de 18 anos de idade.",
        "violence": "Conteúdo que promove ou glorifica violência ou celebra o sofrimento ou humilhação de outros.",
        "violence/graphic": "Conteúdo violento que retrata morte, violência ou lesão física grave em detalhes gráficos extremos.",
    }
    
    # Chama o serviço de Moderação da OpenAI
    response = openai.Moderation.create(input=question)
    
    # Verifica se a pergunta foi sinalizada
    if response.results[0].flagged:
        # Obtém as categorias sinalizadas e gera uma mensagem de erro
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    
    # Mantém o histórico de perguntas e respostas anteriores
    previous_questions_and_answers = []
    
    while True:
        # Pergunta ao usuário qual é a sua pergunta
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "O que posso ajudar?: " + Style.RESET_ALL
        )
        
        # Verifica se a pergunta é segura
        errors = get_moderation(new_question)
        if errors:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Desculpe, sua pergunta não passou na verificação de moderação:"
            )
            for error in errors:
                print(error)
            print(Style.RESET_ALL)
            continue
        
        # Obtém a resposta do bot
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        # Adiciona a nova pergunta e resposta à lista de perguntas e respostas anteriores
        previous_questions_and_answers.append((new_question, response))

        # Imprime a resposta
        print(Fore.CYAN + Style.BRIGHT + "Aqui está: " + Style.NORMAL + response)


if __name__ == "__main__":
    main()
