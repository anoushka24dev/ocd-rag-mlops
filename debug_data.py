import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

df = pd.read_csv("data/raw/ocd_eval_train_500.csv")

print("Label distribution in train:")
print(df[df["split"] == "train"]["label"].value_counts())

print("\nLabel distribution in eval:")
print(df[df["split"] == "eval"]["label"].value_counts())

train_df = df[df["split"] == "train"]
eval_df = df[df["split"] == "eval"]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

pipeline.fit(train_df["text"], train_df["label"])
preds = pipeline.predict(eval_df["text"])

print("\nFull classification report:")
print(classification_report(eval_df["label"], preds))

print("\nSample predictions:")
for text, true, pred in zip(eval_df["text"][:5], eval_df["label"][:5], preds[:5]):
    print(f"TRUE: {true} | PRED: {pred}")
    print(f"TEXT: {text[:100]}\n")