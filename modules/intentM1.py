import re
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

# ── Train classifier ──────────────────────────────────────────────────────────
df = pd.read_csv("data/raw/ocd_eval_train_500.csv")
train_df = df[df["split"] == "train"]

# Balance the classes by undersampling majority
comp = train_df[train_df["label"] == "Compulsion"]
rass = train_df[train_df["label"] == "Reassurance"]
min_count = min(len(comp), len(rass))

train_balanced = pd.concat([
    comp.sample(min_count, random_state=42),
    rass.sample(min_count, random_state=42)
])

X_train = train_balanced["text"].tolist()
y_train = train_balanced["label"].tolist()

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
    ("clf",   LogisticRegression(max_iter=1000, class_weight="balanced"))
])

pipeline.fit(X_train, y_train)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

def detect_intent(query):
    q = clean_text(query)
    prediction = pipeline.predict([q])[0]
    return prediction.lower()