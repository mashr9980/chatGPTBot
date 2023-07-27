from flask import Flask, jsonify, request, render_template
from chat_gpt_api import ChatGPTBotAPI

app = Flask(__name__)

gpt_bot = ChatGPTBotAPI(api_key="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", prompts_file_path="prompts.txt")

gpt_bot.initialize_gpt3()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/create_prompt", methods=["POST"])
def create_prompt():
    data = request.get_json()
    prompt = data.get("prompt")
    prompt_index = gpt_bot.create_prompt(prompt)
    return jsonify({"prompt_index": prompt_index}), 200


@app.route("/get_prompt", methods=["GET"])
def get_prompt():
    prompt_index = int(request.args.get("prompt_index"))
    prompt = gpt_bot.read_prompt(prompt_index)
    return jsonify(prompt), 200


@app.route("/update_prompt", methods=["PUT"])
def update_prompt():
    data = request.get_json()
    prompt_index = data.get("prompt_index")
    new_prompt = data.get("new_prompt")
    result = gpt_bot.update_prompt(prompt_index, new_prompt)
    return jsonify({"result": result}), 200


@app.route("/delete_prompt", methods=["DELETE"])
def delete_prompt():
    data = request.get_json()
    prompt_index = data.get("prompt_index")
    result = gpt_bot.delete_prompt(prompt_index)
    return jsonify({"result": result}), 200


@app.route("/get_all_prompts", methods=["GET"])
def get_all_prompts():
    prompts = gpt_bot.prompts
    return jsonify({"prompts": prompts}), 200


if __name__ == "__main__":
    app.run(debug=True)
