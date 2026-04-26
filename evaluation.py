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

# -----------------------------------
# IMPORT YOUR INTENT FUNCTION
# Adjust if function name differs
# -----------------------------------

from modules.intentM1 import detect_intent


import pandas as pd

df = pd.read_csv("data/raw/ocd_eval_train_500.csv")
df = df[df["split"] == "eval"]

test_data = [
    (row["text"], 1 if row["label"] == "Reassurance" else 0)
    for _, row in df.iterrows()
]


# ---------------------------
# Collect predictions
# ---------------------------

y_true=[]
y_pred=[]
y_scores=[]

for query,label in test_data:

    pred = detect_intent(query)

    # assuming your function returns strings
    if pred.lower() == "reassurance":
        prediction = 1
        confidence = 0.9
    else:
        prediction = 0
        confidence = 0.2

    y_true.append(label)
    y_pred.append(prediction)
    y_scores.append(confidence)



# ---------------------------
# Metrics
# ---------------------------

print("\n--- Evaluation Metrics ---\n")

acc=accuracy_score(y_true,y_pred)
prec=precision_score(y_true,y_pred)
rec=recall_score(y_true,y_pred)
f1=f1_score(y_true,y_pred)

print("Accuracy:",round(acc,3))
print("Precision:",round(prec,3))
print("Recall:",round(rec,3))
print("F1 Score:",round(f1,3))


# ---------------------------
# Confusion Matrix
# ---------------------------

cm=confusion_matrix(y_true,y_pred)

disp=ConfusionMatrixDisplay(
confusion_matrix=cm,
display_labels=["Compulsion","Reassurance"]
)

disp.plot()
plt.title("Confusion Matrix")
plt.show()


# ---------------------------
# ROC Curve
# ---------------------------

fpr,tpr,_=roc_curve(y_true,y_scores)
roc_auc=auc(fpr,tpr)

plt.figure()
plt.plot(
fpr,
tpr,
label=f"AUC={roc_auc:.3f}"
)

plt.plot(
[0,1],
[0,1],
linestyle='--'
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.show()

print("AUC:",round(roc_auc,3))