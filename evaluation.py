import mlflow
import mlflow.sklearn
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("OCD RAG Chatbot")

import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc
)
import pandas as pd
from modules.intentM1 import detect_intent, pipeline

with mlflow.start_run(run_name="TF-IDF + Logistic Regression"):

    # ── Load eval data ────────────────────────────────────────────────────────
    df = pd.read_csv("data/raw/ocd_eval_train_500.csv")
    df = df[df["split"] == "eval"]

    test_data = [
        (row["text"], 1 if row["label"] == "Reassurance" else 0)
        for _, row in df.iterrows()
    ]

    # ── Collect predictions ───────────────────────────────────────────────────
    y_true = []
    y_pred = []
    y_scores = []

    for query, label in test_data:
        pred = detect_intent(query)

        if pred.lower() == "reassurance":
            prediction = 1
            confidence = 0.9
        else:
            prediction = 0
            confidence = 0.2

        y_true.append(label)
        y_pred.append(prediction)
        y_scores.append(confidence)

    # ── Metrics ───────────────────────────────────────────────────────────────
    acc  = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec  = recall_score(y_true, y_pred)
    f1   = f1_score(y_true, y_pred)

    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)

    print("\n--- Evaluation Metrics ---\n")
    print("Accuracy :", round(acc, 3))
    print("Precision:", round(prec, 3))
    print("Recall   :", round(rec, 3))
    print("F1 Score :", round(f1, 3))
    print("AUC      :", round(roc_auc, 3))

    # ── Log metrics to MLflow ─────────────────────────────────────────────────
    mlflow.log_metric("accuracy",  acc)
    mlflow.log_metric("precision", prec)
    mlflow.log_metric("recall",    rec)
    mlflow.log_metric("f1_score",  f1)
    mlflow.log_metric("auc",       roc_auc)

    # ── Log parameters ────────────────────────────────────────────────────────
    mlflow.log_param("model",        "Logistic Regression")
    mlflow.log_param("vectorizer",   "TF-IDF")
    mlflow.log_param("ngram_range",  "(1, 2)")
    mlflow.log_param("max_features", 5000)
    mlflow.log_param("dataset_size", len(test_data))
    mlflow.log_param("classes",      "Compulsion, Reassurance")

    # ── Log model ─────────────────────────────────────────────────────────────
    mlflow.sklearn.log_model(pipeline, "intent_classifier")

    # ── Confusion Matrix ──────────────────────────────────────────────────────
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Compulsion", "Reassurance"]
    )
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
    plt.show()

    # ── ROC Curve ─────────────────────────────────────────────────────────────
    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC={roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.savefig("roc_curve.png")
    mlflow.log_artifact("roc_curve.png")
    plt.show()

    print("\n✅ MLflow run complete.")