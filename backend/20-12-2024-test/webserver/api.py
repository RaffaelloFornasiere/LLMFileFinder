import os

import tiktoken
import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

import backend.utils as utils
from backend.tree_navigator.tree_navigator import FolderNavigator
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tree = FolderNavigator(
    root_name="jpalioapp",
    root_path="/Users/forna/Documents/me/palio",
)

print(os.getcwd())

tree.load(open("../state.json", "r").read())
model = "qwen2.5-coder-14b-instruct"
objective = "Find the game rest controller file/s"

app_status: dict = {
    "base_url": "http://localhost:1234",
    "tree": tree,
    "path": "/Users/forna/Documents/me/palio/jpalioapp",
    "objective": objective,
    "system_message": open("../messages/system_message.md", "r").read(),
    "user_template_message": open("../messages/user_message.md", "r").read()
}


@app.get('/models')
def get_models():
    base_url = "http://localhost:1234"
    models = utils.get_models(base_url)
    models = [model['id'] for model in models['data']]
    models.remove('text-embedding-nomic-embed-text-v1.5')
    return {
        "status": "SUCCESS",
        "data": models
    }


@app.post("/new_tree")
def new():
    global app_status
    main_folder = app_status["path"].split("/")[-1]
    pwd = '/'.join(app_status["path"].split("/")[:-1])
    app_status["tree"] = FolderNavigator(main_folder, pwd)


@app.post("/path")
async def set_path(info: Request):
    global app_status
    data = await info.json()
    app_status["path"] = data["path"]
    return {
        "status": "SUCCESS",
        "data": app_status["path"]
    }


@app.get("/app_status")
async def get_app_status():
    global app_status
    return {
        "status": "SUCCESS",
        "data": app_status
    }


@app.post("/app_status")
async def set_app_status(info: Request):
    global app_status
    data = await info.json()
    app_status = data
    with open("../messages/system_message.md", "w") as f:
        f.write(app_status["system_message"])
    with open("../messages/user_message.md", "w") as f:
        f.write(app_status["user_template_message"])
    return {
        "status": "SUCCESS",
        "data": app_status
    }


@app.get("/get_next_action")
async def get_next_action():
    global app_status

    system_message = app_status["system_message"]
    examples = await get_examples()
    examples = examples["data"]

    system_message = system_message.replace("{{examples}}", "\n---\n\n".join(examples))

    user_message = app_status["user_template_message"]
    user_message = user_message.format(
        tree=app_status["tree"].print(),
        operation_history=app_status["tree"].action_history,
        objective=app_status["objective"])

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    response = utils.get_response(messages, model, app_status["base_url"])
    response_text = utils.parse_response_text(response)
    action, errors, warning = tree.parse(response_text)
    return {
        "status": "SUCCESS",
        "data": {"action": action,
                 "errors": errors,
                 "warnings": warning}
    }


@app.post("/run_action")
async def run_action(info: Request):
    global app_status
    action = await info.json()
    app_status["tree"].run(action)
    app_status["tree"].persist()

    return {
        "status": "SUCCESS",
        "data": app_status
    }


@app.post("/examples")
async def save_example(info: Request):
    ### highly inefficient, but it's just for testing

    examples = await info.json()
    ### remove old examples
    files = os.listdir("../examples")
    for file in files:
        os.remove(f"../examples/{file}")

    ### save new examples
    for i, example in enumerate(examples):
        with open(f"../examples/{i}.md", "w") as f:
            f.write(example)

    return {
        "status": "SUCCESS",
    }


@app.get("/examples")
async def get_examples():
    files = os.listdir("../examples")
    files.sort()
    examples = [open(f"../examples/{file}", "r").read() for file in files]
    return {
        "status": "SUCCESS",
        "data": examples
    }


@app.post("/token_count")
async def get_token_count(info: Request):
    text = (await info.json())['text']
    enc = tiktoken.encoding_for_model("gpt-4o")
    tokens = enc.encode(text)
    return {
        "status": "SUCCESS",
        "data": len(tokens)
    }


if __name__ == '__main__':
    uvicorn.run("api:app", port=8080, host="0.0.0.0", reload=True)
