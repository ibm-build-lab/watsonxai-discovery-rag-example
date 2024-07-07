"""
Simple RAG use case implementation
"""

import os
from dotenv import load_dotenv
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model

load_dotenv()

# discovery env variables
IBM_DISC_API_KEY = os.getenv('IBM_DISC_API_KEY')
IBM_DISC_PROJ_ID = os.getenv('IBM_DISC_PROJ_ID')
IBM_DISC_SERVICE_URL = os.getenv('IBM_DISC_SERVICE_URL')
IBM_DISC_COLL_ID = os.getenv('IBM_DISC_COLL_ID')

# watsonx.ai env variables
IBM_WX_API_KEY= os.getenv('IBM_WX_API_KEY')
IBM_WX_PROJ_ID=os.getenv('IBM_WX_PROJ_ID')
IBM_WX_SERVICE_URL=os.getenv('IBM_WX_SERVICE_URL')

# authentication with services
authenticator = IAMAuthenticator(IBM_DISC_API_KEY)
discovery = DiscoveryV2(version='2020-08-30', authenticator=authenticator)
discovery.set_service_url(IBM_DISC_SERVICE_URL)
discovery.set_disable_ssl_verification(True)
ai_credentials = Credentials(
    url = IBM_WX_SERVICE_URL,
    api_key = IBM_WX_API_KEY
)

# question you are asking
QUERY = 'What is GPT?'

# the set of instructions given to an llm
PROMPT_TEMPLATE = '''
CONTEXT:
%s

QUESTION:
%s

INSTRUCTIONS:
Answer the user's QUESTION using the CONTEXT text above.
Keep your answer grounded in the facts of the CONTEXT.
If the CONTEXT doesn't contain the facts to answer the QUESTION return "I don't know".

ANSWER:
'''

# get passages from discovery
passage_list = discovery.query(
    project_id=IBM_DISC_PROJ_ID,
    natural_language_query=QUERY,
    count=5,
    collection_ids=[IBM_DISC_COLL_ID],
    similar={
        "fields": ["text"]
    },
    passages={
        "enabled": True,
        "per_document": True,
        "find_answers": True,
        "max_answers_per_passage": 1,
        "characters": 250
    }
).get_result()['results']

# wrap into singular string
passage_text = '\n\n'.join(list(map(
    lambda x: '\n\n'.join(map(lambda p: p['passage_text'], x['document_passages'])), 
    passage_list
)))

# LLM parameter definitions
model = Model(
    model_id="meta-llama/llama-2-70b-chat",
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "temperature": 0,
        "min_new_tokens": 35,
        "repetition_penalty": 1.1,
        "stop_sequences": ["\n\n"]
    },
    project_id=IBM_WX_PROJ_ID,
    credentials=ai_credentials
)

# take passages and question and combine them with prompt
final_prompt = PROMPT_TEMPLATE % ( passage_text, QUERY )

# invoke LLM and get answer
output = model.generate_text(prompt=final_prompt, guardrails=False)

print(f"Question: {QUERY}\n")
print(f"Answer:\n{output}")
