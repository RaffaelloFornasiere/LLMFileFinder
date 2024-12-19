### use langchain to call local server that hosts LLM using the OpenAI API
### and return the response to the user

from langchain_openai import ChatOpenAI


# curl http://localhost:1234/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "meta-llama-3.1-8b-instruct",
#     "messages": [
#       { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
#       { "role": "user", "content": "What day is it today?" }
#     ],
#     "temperature": 0.7,
#     "max_tokens": -1,
#     "stream": false
# }'
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1/chat/completions",
    model="meta-llama-3.1-8b-instruct",
    openai_api_key="sk-"
)
