import os

import numpy
import numpy as np
from fastapi import FastAPI, Request
import uvicorn
from backend.actions.actions import FileNavigator
import backend.utils as utils
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


tree = FileNavigator("jpalioapp", "/Users/forna/Documents/me/palio")
tree.tree = {'name': 'jpalioapp',
             'expanded': False,
             'children': [{'name': '.husky', 'children': [], 'expanded': False},
                          {'name': '.DS_Store', 'size': '6.0KiB', 'state': 'unopened'},
                          {'name': 'tsconfig.app.json', 'size': '220.0B', 'state': 'unopened'},
                          {'name': 'mvnw.cmd', 'size': '6.8KiB', 'state': 'unopened'},
                          {'name': 'npmw.cmd', 'size': '1.1KiB', 'state': 'unopened'},
                          {'name': 'target', 'children': [], 'expanded': False},
                          {'name': '.yo-rc.json', 'size': '1.4KiB', 'state': 'unopened'},
                          {'name': 'node_modules', 'children': [], 'expanded': False},
                          {'name': 'pom.xml', 'size': '59.3KiB', 'state': 'unopened'},
                          {'name': '.devcontainer', 'children': [], 'expanded': False},
                          {'name': '.prettierignore', 'size': '134.0B', 'state': 'unopened'},
                          {'name': '.editorconfig', 'size': '489.0B', 'state': 'unopened'},
                          {'name': 'README.md', 'size': '10.4KiB', 'state': 'unopened'},
                          {'name': 'jpalioapp.jdl', 'size': '465.0B', 'state': 'unopened'},
                          {'name': 'angular.json', 'size': '3.3KiB', 'state': 'unopened'},
                          {'name': 'webpack', 'children': [], 'expanded': False},
                          {'name': 'sonar-project.properties', 'size': '3.3KiB', 'state': 'unopened'},
                          {'name': 'ngsw-config.json', 'size': '530.0B', 'state': 'unopened'},
                          {'name': '.gitignore', 'size': '2.0KiB', 'state': 'unopened'},
                          {'name': 'package-lock.json', 'size': '878.4KiB', 'state': 'unopened'},
                          {'name': 'package.json', 'size': '7.2KiB', 'state': 'unopened'},
                          {'name': '.mvn', 'children': [], 'expanded': False},
                          {'name': '.jhipster', 'children': [], 'expanded': False},
                          {'name': '.prettierrc', 'size': '231.0B', 'state': 'unopened'},
                          {'name': '.gitattributes', 'size': '3.3KiB', 'state': 'unopened'},
                          {'name': 'checkstyle.xml', 'size': '924.0B', 'state': 'unopened'},
                          {'name': 'npmw', 'size': '973.0B', 'state': 'unopened'},
                          {'name': 'tsconfig.json', 'size': '906.0B', 'state': 'unopened'},
                          {'name': 'venv', 'children': [], 'expanded': False},
                          {'name': '.git', 'children': [], 'expanded': False},
                          {'name': '.lintstagedrc.cjs', 'size': '112.0B', 'state': 'unopened'},
                          {'name': 'mvnw', 'size': '10.1KiB', 'state': 'unopened'},
                          {'name': 'openapi.json', 'size': '96.3KiB', 'state': 'unopened'},
                          {'name': 'eslint.config.mjs', 'size': '4.5KiB', 'state': 'unopened'},
                          {'name': 'tsconfig.spec.json', 'size': '195.0B', 'state': 'unopened'},
                          {'name': 'jest.conf.js', 'size': '1.1KiB', 'state': 'unopened'},
                          {'name': '.idea', 'children': [], 'expanded': False},
                          {'name': 'src',
                           'children': [{'name': 'test', 'children': [], 'expanded': False},
                                        {'name': 'main',
                                         'children': [{'name': 'docker', 'children': [], 'expanded': False},
                                                      {'name': 'LLM_I', 'children': [], 'expanded': False},
                                                      {'name': 'resources', 'children': [], 'expanded': False},
                                                      {'name': 'webapp', 'children': [], 'expanded': False},
                                                      {'name': 'java',
                                                       'children': [{'name': 'it',
                                                                     'children': [{'name': 'rf',
                                                                                   'children': [{'name': 'jpalioapp',
                                                                                                 'children': [{
                                                                                                     'name': 'GeneratedByJHipster.java',
                                                                                                     'size': '405.0B',
                                                                                                     'state': 'opened'},
                                                                                                     {
                                                                                                         'name': 'repository',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'config',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'security',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'web',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'management',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'aop',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'JpalioappApp.java',
                                                                                                         'size': '4.2KiB',
                                                                                                         'state': 'unopened'},
                                                                                                     {
                                                                                                         'name': 'ApplicationWebXml.java',
                                                                                                         'size': '805.0B',
                                                                                                         'state': 'unopened'},
                                                                                                     {
                                                                                                         'name': 'service',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'domain',
                                                                                                         'children': [],
                                                                                                         'expanded': False},
                                                                                                     {
                                                                                                         'name': 'package-info.java',
                                                                                                         'size': '54.0B',
                                                                                                         'state': 'unopened'}],
                                                                                                 'expanded': False}],
                                                                                   'expanded': False}],
                                                                     'expanded': False}],
                                                       'expanded': False}],
                                         'expanded': False}],
                           'expanded': False}]}

operation_history = []
system_message = open("../system_message.md", "r").read()
user_message = open("../user_message.md", "r").read()
model = "qwen2.5-coder-14b-instruct"
objective = "Find the game rest controller file/s"

app_status: dict = {
    "tree": tree.tree,
    "path": "/Users/forna/Documents/me/palio/jpalioapp",
    "objective": objective,
    "history": [
        {"action": "expand", "node": "jpalioapp",
         "short_comment": "The 'jpalioapp' folder is likely to contain the game rest controller file/s. Expanding it "
                          "will reveal its contents."},
        {"action": "expand", "node": "jpalioapp/src",
         "short_comment": "The 'src' folder is likely to contain the source code for the game rest controller. Expanding it will reveal its contents."},
        {"action": "expand", "node": "jpalioapp/src/main",
         "short_comment": "The 'src/main' folder is likely to contain the main source code for the application, including the game rest controller. Expanding it will reveal its contents."},
        {"action": "expand", "node": "jpalioapp/src/main/java",
         "short_comment": "The 'src/main/java' folder is a common location for Java source code, including controllers. Expanding it will help locate the game rest controller file/s."},
        {"action": "expand", "node": "jpalioapp/src/main/java/it",
         "short_comment": "The 'src/main/java/it' folder is likely to contain integration test files that may reference the game rest controller. Expanding this will help identify relevant controller files."},
        {"action": "expand", "node": "jpalioapp/src/main/java/it/rf",
         "short_comment": "The 'src/main/java/it/rf' folder is the most specific path we have identified so far for potentially finding the game rest controller file. Expanding this will help us locate the relevant controller files."},
    ],
    "system_message": system_message,
    "user_template_message": user_message
}


@app.get('/models')
def get_models():
    # GET /api/v0/models - List available models
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
    app_status["tree"] = FileNavigator(main_folder, pwd)


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
    with open("../system_message.md", "w") as f:
        f.write(app_status["system_message"])
    with open("../user_message.md", "w") as f:
        f.write(app_status["user_template_message"])
    return {
        "status": "SUCCESS",
        "data": app_status
    }


@app.post("/compute_action")
async def compute_action(info: Request):
    global app_status
    data = await info.json()
    response = utils.get_response(data["messages"], model, base_url)
    response_text = utils.parse_response_text(response)
    action, errors, warnings = app_status["tree"].parse(response_text)
    app_status["tree"].run(action)
    app_status["history"].append(action)
    return {
        "status": "SUCCESS",
        "data": {
            "action": action,
            "errors": errors,
            "warnings": warnings
        }
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



if __name__ == '__main__':
    uvicorn.run("api:app", port=8080, host="0.0.0.0", reload=True)
