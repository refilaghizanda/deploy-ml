import os
import tensorflow as tf
from flask import Flask, request, jsonify
mse = tf.keras.losses.MeanSquaredError()
# Daftarkan fungsi ke serialization Keras jika diperlukan
# mse = MeanSquaredError()

# Inisialisasi Flask
app = Flask(__name__)

# Load models
models = {
    "ambon": tf.keras.models.load_model("models/model_ambon.h5", custom_objects={"mse": mse}),
    "balikpapan": tf.keras.models.load_model("models/model_balikpapan.h5", custom_objects={"mse": mse}),
    "banda_aceh": tf.keras.models.load_model("models/model_banda_aceh.h5", custom_objects={"mse": mse}),
}

@app.route("/", methods=["GET"])
def index():
    return "nice bisa"

@app.route("/predict/<model_name>", methods=["POST"])
def predict(model_name):
    if model_name not in models:
        return jsonify({"error": f"model {model_name} gaada"}), 404

    # Ambil data dari request
    try:
        data = request.json.get("data")
        if not data:
            raise ValueError("data tidak ada")
        
        # Pastikan data berbentuk array 2D (contoh: [[1, 2, 3]])
        data = tf.convert_to_tensor(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Ambil model dan lakukan prediksi
    model = models[model_name]
    prediction = model.predict(data).tolist()

    return jsonify({"prediction": prediction})

@app.route("/predict/<model_name>", methods=["GET"])
def get_model_info(model_name):
    if model_name not in models:
        return jsonify({"error": f"model {model_name} gaada"}), 404

    # Ambil model dan kembalikan arsitektur JSON
    model = models[model_name]
    model_info = model.to_json()
    return jsonify({"model_name": model_name, "architecture": model_info})

if __name__ == "__main__":
    # Ubah host ke 0.0.0.0 agar bisa diakses di Cloud Run
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
