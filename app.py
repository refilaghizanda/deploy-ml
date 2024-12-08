import os
import tensorflow as tf
from flask import Flask, request, jsonify
mse = tf.keras.losses.MeanSquaredError()

app = Flask(__name__)

# model masih 3s
models = {
    "ambon": tf.keras.models.load_model("models/model_ambon.h5", custom_objects={"mse": mse}),
    "balikpapan": tf.keras.models.load_model("models/model_balikpapan.h5", custom_objects={"mse": mse}),
    "banda_aceh": tf.keras.models.load_model("models/model_banda_aceh.h5", custom_objects={"mse": mse}),
}

# @app.route("/", methods=["GET"])
# def index():
#     return "nice bisa"

@app.route("/", methods=["GET"])
def index():
    model_names = list(models.keys()) 
    return jsonify({"models": model_names})

@app.route("/predict/<model_name>", methods=["GET"])
def get_model_info(model_name):
    if model_name not in models:
        return jsonify({"error": f"{model_name} tidak ada"}), 404

    # ambil model and return json
    model = models[model_name]
    model_info = model.to_json()
    return jsonify({"model_name": model_name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
