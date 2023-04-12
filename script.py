import os
import openai
import tiktoken
import json


class Params():
    MODEL = "text-davinci-003"
    # MODEL = "gpt-3.5-turbo"
    TEMPERATURE = 0.5

def main():
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        openai.organization = os.getenv("OPENAI_ORG_KEY")
    except Exception as e:
        print(f"Error loading OpenAI organization: {e} \nMoving on...")
    
    source = input("Article source: ")
    wanted_bias = input("Wanted translation bias: ")
    prompt = gen_prompt(source, wanted_bias)
    
    enc = tiktoken.encoding_for_model("text-davinci-003")
    max_tokens = 4000 - len(enc.encode(prompt))
    print(max_tokens)

    response = openai.Completion.create(model=Params.MODEL,
                                        prompt=prompt,
                                        temperature=Params.TEMPERATURE,
                                        max_tokens=max_tokens)
    print(response.choices[0].text)
    return 0


def gen_prompt(inital_source, wanted_bias):
    with open('sources.json', 'r', encoding='utf8') as f:
        source_list = json.load(f)
    
    source_bias = source_list[inital_source]
    
    prompt = f'The following is an article written by {inital_source}, a {source_bias} news source. Please take \
                the same basic information the article is presenting, but \
                turn it into an article that would be written by a {wanted_bias} news source. Additionally, \
                after your translation, provide an explanation for specific phrases or words you \
                changed, or any reasonings you had for making any changes you did. \n\n Present all of this in \
                a JSON string, where the translated article has the key "article". The phrases changed will \
                be a list with the key "changes" and within the list, each phrase will have the original phrase \
                (key "original"), the changed phrase (key "new") and the explanation (key "explanation").\
                \n\n The article is below: \n\n'
    
    article = input("Please copy and paste the article text: ")
    
    prompt += article
    return prompt


if __name__ == '__main__':
    main()
