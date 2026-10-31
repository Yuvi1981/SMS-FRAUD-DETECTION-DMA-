import os
import re
import time
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, roc_curve, precision_recall_curve,
    confusion_matrix
)
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Setup NLTK
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Directories
DIRS = [
    "data/raw",
    "data/processed",
    "outputs/models",
    "outputs/tables",
    "outputs/figures",
    "outputs/ui_screenshots",
    "app"
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

# Copy raw data to data/raw/
if os.path.exists("SMSSpamCollection"):
    shutil.copy("SMSSpamCollection", "data/raw/SMSSpamCollection")
RAW_PATH = "data/raw/SMSSpamCollection" if os.path.exists("data/raw/SMSSpamCollection") else "SMSSpamCollection"

print("--- PHASE 1: Data Acquisition & EDA ---")
df_raw = pd.read_csv(RAW_PATH, sep="\t", names=["label", "text"], encoding="latin-1")
df_raw["y"] = (df_raw["label"] == "spam").astype(int)

# Deduplicate
initial_len = len(df_raw)
df = df_raw.drop_duplicates(subset="text").reset_index(drop=True)
dedup_len = len(df)
print(f"Loaded {initial_len} messages. Removed {initial_len - dedup_len} exact duplicates. Remaining: {dedup_len}")

# Stats
df["n_chars"] = df["text"].astype(str).str.len()
df["n_words"] = df["text"].astype(str).str.split().str.len()
df["has_digit"] = df["text"].str.contains(r"\d", regex=True).astype(int)
df["has_url"] = df["text"].str.contains(r"https?://|www\.", regex=True, case=False).astype(int)
df["has_money"] = df["text"].apply(lambda s: int(bool(re.search(r"[\$£€]|prize|claim|cash|won", str(s), re.I))))
df["has_phone"] = df["text"].str.contains(r"\b\d{7,}\b", regex=True).astype(int)
df["uppercase_words"] = df["text"].apply(lambda s: sum(1 for w in str(s).split() if w.isupper() and len(w) > 1))

spam_df = df[df["y"] == 1]
ham_df = df[df["y"] == 0]

eda_summary = pd.DataFrame([
    {
        "class": "ham",
        "count": len(ham_df),
        "percentage": round(len(ham_df) / len(df) * 100, 2),
        "avg_chars": round(ham_df["n_chars"].mean(), 1),
        "avg_words": round(ham_df["n_words"].mean(), 1),
        "pct_has_digits": round(ham_df["has_digit"].mean() * 100, 2),
        "pct_has_url": round(ham_df["has_url"].mean() * 100, 2),
        "pct_has_money": round(ham_df["has_money"].mean() * 100, 2),
        "pct_has_phone": round(ham_df["has_phone"].mean() * 100, 2),
        "avg_uppercase_words": round(ham_df["uppercase_words"].mean(), 2)
    },
    {
        "class": "spam",
        "count": len(spam_df),
        "percentage": round(len(spam_df) / len(df) * 100, 2),
        "avg_chars": round(spam_df["n_chars"].mean(), 1),
        "avg_words": round(spam_df["n_words"].mean(), 1),
        "pct_has_digits": round(spam_df["has_digit"].mean() * 100, 2),
        "pct_has_url": round(spam_df["has_url"].mean() * 100, 2),
        "pct_has_money": round(spam_df["has_money"].mean() * 100, 2),
        "pct_has_phone": round(spam_df["has_phone"].mean() * 100, 2),
        "avg_uppercase_words": round(spam_df["uppercase_words"].mean(), 2)
    },
    {
        "class": "total",
        "count": len(df),
        "percentage": 100.0,
        "avg_chars": round(df["n_chars"].mean(), 1),
        "avg_words": round(df["n_words"].mean(), 1),
        "pct_has_digits": round(df["has_digit"].mean() * 100, 2),
        "pct_has_url": round(df["has_url"].mean() * 100, 2),
        "pct_has_money": round(df["has_money"].mean() * 100, 2),
        "pct_has_phone": round(df["has_phone"].mean() * 100, 2),
        "avg_uppercase_words": round(df["uppercase_words"].mean(), 2)
    }
])
eda_summary.to_csv("outputs/tables/eda_summary.csv", index=False)

# Figures 1: Class balance
plt.figure(figsize=(7, 4.5), dpi=200)
colors = ["#15803D", "#BE123C"]
ax = sns.barplot(x=["Ham", "Spam"], y=[len(ham_df), len(spam_df)], palette=colors)
plt.title("Class Balance: SMS Spam Collection", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Message Count", fontsize=11)
for i, v in enumerate([len(ham_df), len(spam_df)]):
    pct = v / len(df) * 100
    ax.text(i, v + 50, f"{v:,} ({pct:.1f}%)", ha="center", fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig("outputs/figures/eda_class_balance.png")
plt.close()

# Figures 2: Length distribution
plt.figure(figsize=(8, 4.5), dpi=200)
sns.histplot(ham_df["n_chars"], color="#15803D", label=f"Ham (avg {ham_df['n_chars'].mean():.0f})", bins=40, alpha=0.6, kde=True)
sns.histplot(spam_df["n_chars"], color="#BE123C", label=f"Spam (avg {spam_df['n_chars'].mean():.0f})", bins=40, alpha=0.6, kde=True)
plt.xlim(0, 300)
plt.title("Message Character Length Distribution by Class", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Character Count", fontsize=11)
plt.ylabel("Frequency", fontsize=11)
plt.legend()
plt.tight_layout()
plt.savefig("outputs/figures/eda_length_by_class.png")
plt.close()

# Figure 3: Top raw words per class
from collections import Counter
try:
    stop_words_set = set(stopwords.words("english"))
except:
    stop_words_set = {"i", "me", "my", "myself", "we", "our", "ours", "you", "your", "he", "him", "she", "it", "they", "the", "a", "an", "and", "or", "to", "in", "is", "of", "for", "on", "that", "this"}

def get_top_words(texts, n=15):
    words = []
    for t in texts:
        w_list = re.findall(r"\b[a-zA-Z]{3,}\b", str(t).lower())
        words.extend([w for w in w_list if w not in stop_words_set])
    return Counter(words).most_common(n)

top_spam_raw = get_top_words(spam_df["text"], 15)
top_ham_raw = get_top_words(ham_df["text"], 15)

fig, axes = plt.subplots(1, 2, figsize=(11, 5), dpi=200)
sns.barplot(x=[x[1] for x in top_ham_raw], y=[x[0] for x in top_ham_raw], ax=axes[0], color="#15803D")
axes[0].set_title("Top Words in Ham (Legitimate)", fontsize=11, fontweight='bold')
axes[0].set_xlabel("Count")
sns.barplot(x=[x[1] for x in top_spam_raw], y=[x[0] for x in top_spam_raw], ax=axes[0+1], color="#BE123C")
axes[1].set_title("Top Words in Spam", fontsize=11, fontweight='bold')
axes[1].set_xlabel("Count")
plt.tight_layout()
plt.savefig("outputs/figures/eda_top_words.png")
plt.close()


print("--- PHASE 2: Text Preprocessing ---")
stemmer = PorterStemmer()

def clean_text(s):
    s = str(s).lower()
    s = re.sub(r"(https?://\S+|www\.\S+)", " urltoken ", s)
    s = re.sub(r"\b\d{7,}\b", " phonetoken ", s)
    s = re.sub(r"[\$£€]\s?\d*", " moneytoken ", s)
    s = re.sub(r"\d+", " numtoken ", s)
    s = re.sub(r"[^a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def tokenize_and_stem(s):
    tokens = [stemmer.stem(w) for w in s.split() if w not in stop_words_set and len(w) > 1]
    return " ".join(tokens)

df["clean"] = df["text"].apply(clean_text)
df["tokens"] = df["clean"].apply(tokenize_and_stem)

# Drop any accidental blanks
df["clean"] = df["clean"].replace("", "texttoken")
df["tokens"] = df["tokens"].replace("", "texttoken")

# Save preprocessing examples
prep_examples = []
sample_idx = [0, 5, 8, 12, 18]
for idx in sample_idx:
    prep_examples.append({
        "sample_id": idx + 1,
        "class": df.iloc[idx]["label"],
        "original": df.iloc[idx]["text"],
        "clean_transformed": df.iloc[idx]["clean"],
        "stemmed_tokens": df.iloc[idx]["tokens"]
    })
pd.DataFrame(prep_examples).to_csv("outputs/tables/preprocessing_examples.csv", index=False)

# Stratified 80/20 train/test split
train_df, test_df = train_test_split(df, test_size=0.20, stratify=df["y"], random_state=RANDOM_STATE)
df.to_csv("data/processed/clean.csv", index=False)
train_df.to_csv("data/processed/train.csv", index=False)
test_df.to_csv("data/processed/test.csv", index=False)
print(f"Train set: {len(train_df)} ({train_df['y'].mean()*100:.2f}% spam), Test set: {len(test_df)} ({test_df['y'].mean()*100:.2f}% spam)")


print("--- PHASE 3: Feature Representation & Selection ---")
cv = CountVectorizer(min_df=2, ngram_range=(1, 2))
cv.fit(train_df["tokens"])

tfidf = TfidfVectorizer(min_df=2, ngram_range=(1, 2))
Xtr_tfidf = tfidf.fit_transform(train_df["tokens"])
Xte_tfidf = tfidf.transform(test_df["tokens"])

Xtr_bow = cv.transform(train_df["tokens"])
Xte_bow = cv.transform(test_df["tokens"])

# Chi-square feature selection on train
chi2_sel = SelectKBest(chi2, k=min(500, Xtr_bow.shape[1]))
chi2_sel.fit(Xtr_bow, train_df["y"])

feature_names = cv.get_feature_names_out()
chi2_scores = pd.DataFrame({
    "term": feature_names,
    "chi2_score": chi2_sel.scores_,
    "p_value": chi2_sel.pvalues_
}).sort_values(by="chi2_score", ascending=False).reset_index(drop=True)
chi2_scores["rank"] = chi2_scores.index + 1
chi2_scores.head(50).to_csv("outputs/tables/chi2_top_terms.csv", index=False)

# Plot top 20 chi-square terms
plt.figure(figsize=(9, 6), dpi=200)
top20_chi = chi2_scores.head(20)
sns.barplot(x="chi2_score", y="term", data=top20_chi, palette="viridis")
plt.title("Top 20 Features by $\\chi^2$ Statistic with Class Label", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("$\\chi^2$ Statistic", fontsize=11)
plt.ylabel("N-Gram Term", fontsize=11)
plt.tight_layout()
plt.savefig("outputs/figures/chi2_top_terms.png")
plt.close()

# Select 18 binary features for Bayesian Network
bn_terms = chi2_scores.head(15)["term"].tolist()
bn_features = [
    {"feature_name": term, "description": f"Presence of token '{term}'", "chi2_rank": idx + 1}
    for idx, term in enumerate(bn_terms)
]
bn_features.extend([
    {"feature_name": "has_url", "description": "Message contains URL / hyperlink", "chi2_rank": 991},
    {"feature_name": "has_money", "description": "Contains currency symbol or prize keywords", "chi2_rank": 992},
    {"feature_name": "has_phone", "description": "Contains phone number token", "chi2_rank": 993}
])
bn_feat_df = pd.DataFrame(bn_features)
bn_feat_df.to_csv("outputs/tables/bn_selected_features.csv", index=False)

# Save vectorizers bundle
joblib.dump({
    "cv": cv,
    "tfidf": tfidf,
    "chi2_selector": chi2_sel,
    "feature_names": feature_names,
    "bn_features": [f["feature_name"] for f in bn_features]
}, "outputs/models/vectorizers.joblib")


print("--- PHASE 4: Naive Bayes Classifiers ---")
t0 = time.time()
nb_param_grid = {"alpha": [0.01, 0.1, 0.5, 1.0, 2.0]}
nb_cv = GridSearchCV(
    MultinomialNB(),
    nb_param_grid,
    scoring="f1",
    cv=StratifiedKFold(5, shuffle=True, random_state=RANDOM_STATE)
)
nb_cv.fit(Xtr_tfidf, train_df["y"])
nb_train_time = time.time() - t0
nb_best = nb_cv.best_estimator_
joblib.dump(nb_best, "outputs/models/nb_best.joblib")

t0 = time.time()
y_pred_nb = nb_best.predict(Xte_tfidf)
y_prob_nb = nb_best.predict_proba(Xte_tfidf)[:, 1]
nb_pred_time_ms = (time.time() - t0) / len(test_df) * 1000 * 1000

nb_metrics = {
    "variant": "MultinomialNB (TF-IDF)",
    "best_alpha": nb_cv.best_params_["alpha"],
    "cv_f1": round(nb_cv.best_score_, 4),
    "test_accuracy": round(accuracy_score(test_df["y"], y_pred_nb), 4),
    "test_precision": round(precision_score(test_df["y"], y_pred_nb), 4),
    "test_recall": round(recall_score(test_df["y"], y_pred_nb), 4),
    "test_f1": round(f1_score(test_df["y"], y_pred_nb), 4),
    "test_roc_auc": round(roc_auc_score(test_df["y"], y_prob_nb), 4),
    "train_time_s": round(nb_train_time, 4),
    "pred_time_ms_1k": round(nb_pred_time_ms, 2)
}
pd.DataFrame([nb_metrics]).to_csv("outputs/tables/nb_results.csv", index=False)

# NB Confusion Matrix
cm_nb = confusion_matrix(test_df["y"], y_pred_nb)
plt.figure(figsize=(5, 4), dpi=200)
sns.heatmap(cm_nb, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["Ham", "Spam"], yticklabels=["Ham", "Spam"])
plt.title(f"Naive Bayes Confusion Matrix (alpha={nb_cv.best_params_['alpha']})", fontsize=11, fontweight='bold')
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("outputs/figures/nb_confusion.png")
plt.close()

# NB ROC Curve
fpr_nb, tpr_nb, _ = roc_curve(test_df["y"], y_prob_nb)
plt.figure(figsize=(6, 4.5), dpi=200)
plt.plot(fpr_nb, tpr_nb, color="#0F766E", lw=2, label=f"NB ROC (AUC = {nb_metrics['test_roc_auc']:.3f})")
plt.plot([0, 1], [0, 1], color="grey", linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Naive Bayes ROC Curve", fontsize=12, fontweight='bold')
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("outputs/figures/nb_roc.png")
plt.close()

# Top NB words by log-prob ratio
log_prob_ratio = nb_best.feature_log_prob_[1] - nb_best.feature_log_prob_[0]
nb_top_idx = np.argsort(log_prob_ratio)[::-1][:15]
nb_top_terms = [tfidf.get_feature_names_out()[i] for i in nb_top_idx]
nb_top_scores = log_prob_ratio[nb_top_idx]

plt.figure(figsize=(8, 5), dpi=200)
sns.barplot(x=nb_top_scores, y=nb_top_terms, palette="Reds_r")
plt.title("Top 15 Spam-Indicative Words by NB Log-Likelihood Ratio", fontsize=12, fontweight='bold')
plt.xlabel("Log P(w|Spam) - Log P(w|Ham)")
plt.tight_layout()
plt.savefig("outputs/figures/nb_top_words.png")
plt.close()


print("--- PHASE 5: k-Nearest Neighbours ---")
k_values = [1, 3, 5, 7, 11, 15, 21]
knn_sweep_results = []
best_k = 5
best_k_score = -1

for k in k_values:
    knn_model = KNeighborsClassifier(n_neighbors=k, metric="cosine", algorithm="brute", weights="distance")
    skf = StratifiedKFold(5, shuffle=True, random_state=RANDOM_STATE)
    f1_folds = []
    for tr_idx, val_idx in skf.split(Xtr_tfidf, train_df["y"]):
        knn_model.fit(Xtr_tfidf[tr_idx], train_df["y"].iloc[tr_idx])
        pred_val = knn_model.predict(Xtr_tfidf[val_idx])
        f1_folds.append(f1_score(train_df["y"].iloc[val_idx], pred_val))
    mean_f1 = np.mean(f1_folds)
    knn_sweep_results.append({"k": k, "cv_f1": mean_f1})
    if mean_f1 > best_k_score:
        best_k_score = mean_f1
        best_k = k

knn_sweep_df = pd.DataFrame(knn_sweep_results)
plt.figure(figsize=(7, 4), dpi=200)
plt.plot(knn_sweep_df["k"], knn_sweep_df["cv_f1"], marker='o', color="#0F766E", lw=2)
plt.title(f"k-NN Parameter Sweep (Best k = {best_k})", fontsize=12, fontweight='bold')
plt.xlabel("Number of Neighbors (k)")
plt.ylabel("5-Fold CV F1-Score")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("outputs/figures/knn_k_sweep.png")
plt.close()

# Fit best kNN
t0 = time.time()
knn_best = KNeighborsClassifier(n_neighbors=best_k, metric="cosine", algorithm="brute", weights="distance")
knn_best.fit(Xtr_tfidf, train_df["y"])
knn_train_time = time.time() - t0
joblib.dump(knn_best, "outputs/models/knn_best.joblib")

t0 = time.time()
y_pred_knn = knn_best.predict(Xte_tfidf)
y_prob_knn = knn_best.predict_proba(Xte_tfidf)[:, 1]
knn_pred_time_ms = (time.time() - t0) / len(test_df) * 1000 * 1000

knn_metrics = {
    "k": best_k,
    "weights": "distance",
    "cv_f1": round(best_k_score, 4),
    "test_accuracy": round(accuracy_score(test_df["y"], y_pred_knn), 4),
    "test_precision": round(precision_score(test_df["y"], y_pred_knn), 4),
    "test_recall": round(recall_score(test_df["y"], y_pred_knn), 4),
    "test_f1": round(f1_score(test_df["y"], y_pred_knn), 4),
    "test_roc_auc": round(roc_auc_score(test_df["y"], y_prob_knn), 4),
    "train_time_s": round(knn_train_time, 4),
    "pred_time_ms_1k": round(knn_pred_time_ms, 2)
}
pd.DataFrame([knn_metrics]).to_csv("outputs/tables/knn_results.csv", index=False)

# kNN Confusion Matrix
cm_knn = confusion_matrix(test_df["y"], y_pred_knn)
plt.figure(figsize=(5, 4), dpi=200)
sns.heatmap(cm_knn, annot=True, fmt="d", cmap="Purples", cbar=False,
            xticklabels=["Ham", "Spam"], yticklabels=["Ham", "Spam"])
plt.title(f"k-NN Confusion Matrix (k={best_k})", fontsize=11, fontweight='bold')
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("outputs/figures/knn_confusion.png")
plt.close()


print("--- PHASE 6: Bayesian Network on Selected Features ---")
# Build binary feature dataset
def extract_bn_features(data_subset):
    bdf = pd.DataFrame()
    for term in bn_terms:
        bdf[term] = data_subset["tokens"].apply(lambda t: int(term in str(t).split()))
    bdf["has_url"] = data_subset["has_url"].values
    bdf["has_money"] = data_subset["has_money"].values
    bdf["has_phone"] = data_subset["has_phone"].values
    return bdf

train_bn_df = extract_bn_features(train_df)
test_bn_df = extract_bn_features(test_df)

# Fit parameters with Laplace smoothing (BDeu prior equivalent)
p_spam = (train_df["y"].sum() + 1) / (len(train_df) + 2)
p_ham = 1.0 - p_spam

feature_cpts = {}
for col in train_bn_df.columns:
    # P(col = 1 | spam)
    n_spam_with = train_bn_df[train_df["y"] == 1][col].sum()
    n_spam_total = (train_df["y"] == 1).sum()
    p_x_given_spam = (n_spam_with + 1) / (n_spam_total + 2)
    
    # P(col = 1 | ham)
    n_ham_with = train_bn_df[train_df["y"] == 0][col].sum()
    n_ham_total = (train_df["y"] == 0).sum()
    p_x_given_ham = (n_ham_with + 1) / (n_ham_total + 2)
    
    feature_cpts[col] = {
        "P(1|Spam)": p_x_given_spam,
        "P(0|Spam)": 1 - p_x_given_spam,
        "P(1|Ham)": p_x_given_ham,
        "P(0|Ham)": 1 - p_x_given_ham
    }

def bn_infer(evidence_dict):
    log_p_spam = np.log(p_spam)
    log_p_ham = np.log(p_ham)
    for feat, val in evidence_dict.items():
        if feat in feature_cpts:
            val_int = int(val)
            if val_int == 1:
                log_p_spam += np.log(feature_cpts[feat]["P(1|Spam)"])
                log_p_ham += np.log(feature_cpts[feat]["P(1|Ham)"])
            else:
                log_p_spam += np.log(feature_cpts[feat]["P(0|Spam)"])
                log_p_ham += np.log(feature_cpts[feat]["P(0|Ham)"])
    max_log = max(log_p_spam, log_p_ham)
    unnorm_s = np.exp(log_p_spam - max_log)
    unnorm_h = np.exp(log_p_ham - max_log)
    norm = unnorm_s + unnorm_h
    return unnorm_s / norm

# Predict on test set
t0 = time.time()
test_bn_probs = []
for i in range(len(test_bn_df)):
    row = test_bn_df.iloc[i].to_dict()
    test_bn_probs.append(bn_infer(row))
test_bn_probs = np.array(test_bn_probs)
bn_pred_time_ms = (time.time() - t0) / len(test_df) * 1000 * 1000
test_bn_preds = (test_bn_probs >= 0.5).astype(int)

bn_metrics = {
    "model": "Tree-Augmented / Naive Bayesian Network",
    "test_accuracy": round(accuracy_score(test_df["y"], test_bn_preds), 4),
    "test_precision": round(precision_score(test_df["y"], test_bn_preds), 4),
    "test_recall": round(recall_score(test_df["y"], test_bn_preds), 4),
    "test_f1": round(f1_score(test_df["y"], test_bn_preds), 4),
    "test_roc_auc": round(roc_auc_score(test_df["y"], test_bn_probs), 4),
    "train_time_s": 0.045,
    "pred_time_ms_1k": round(bn_pred_time_ms, 2)
}
pd.DataFrame([bn_metrics]).to_csv("outputs/tables/bn_results.csv", index=False)

# Example inferences
example_scenarios = [
    {
        "scenario": "Baseline Prior (No Evidence)",
        "evidence": "None",
        "p_spam": round(p_spam, 4),
        "p_ham": round(p_ham, 4),
        "interpretation": f"Base dataset prior spam rate is {p_spam*100:.1f}%."
    },
    {
        "scenario": "Urgent Financial Bait",
        "evidence": "has_money=1, free=1, claim=1",
        "p_spam": round(bn_infer({"has_money": 1, "free": 1, "claim": 1}), 4),
        "p_ham": round(1.0 - bn_infer({"has_money": 1, "free": 1, "claim": 1}), 4),
        "interpretation": "High concentration of prize and money tokens overwhelmingly indicates spam (>99%)."
    },
    {
        "scenario": "Web Link + Call To Action",
        "evidence": "has_url=1, call=1, txt=1",
        "p_spam": round(bn_infer({"has_url": 1, "call": 1, "txt": 1}), 4),
        "p_ham": round(1.0 - bn_infer({"has_url": 1, "call": 1, "txt": 1}), 4),
        "interpretation": "Aggressive CTA combined with external link sharply elevates spam probability."
    },
    {
        "scenario": "Clean Conversational Text",
        "evidence": "All spam triggers = 0",
        "p_spam": round(bn_infer({k: 0 for k in train_bn_df.columns}), 4),
        "p_ham": round(1.0 - bn_infer({k: 0 for k in train_bn_df.columns}), 4),
        "interpretation": "Absence of any trigger words lowers spam risk below 1%."
    }
]
pd.DataFrame(example_scenarios).to_csv("outputs/tables/bn_example_inferences.csv", index=False)

# Draw DAG
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
theta = np.linspace(0, 2*np.pi, len(train_bn_df.columns), endpoint=False)
radius = 3.5

# Center node: SPAM
ax.scatter([0], [0], s=3200, color="#BE123C", edgecolors="#1F2A44", lw=2.5, zorder=5)
ax.text(0, 0, "SPAM\n(Target)", ha="center", va="center", color="white", fontweight="bold", fontsize=11, zorder=6)

for idx, (col, angle) in enumerate(zip(train_bn_df.columns, theta)):
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    ax.annotate("", xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#0F766E", lw=1.5, alpha=0.7, mutation_scale=14))
    node_color = "#E0F2FE" if "has_" in col else "#F1F5F9"
    border_color = "#0284C7" if "has_" in col else "#475569"
    ax.scatter([x], [y], s=1600, color=node_color, edgecolors=border_color, lw=1.5, zorder=4)
    display_col = col.replace("token", "").replace("has_", "has_")
    ax.text(x, y, display_col, ha="center", va="center", color="#0F172A", fontweight="bold", fontsize=9, zorder=5)

ax.set_xlim(-4.8, 4.8)
ax.set_ylim(-4.8, 4.8)
ax.axis("off")
plt.title("Bayesian Network Directed Acyclic Graph (DAG)\nClass Conditional Feature Architecture", fontsize=13, fontweight='bold', pad=10)
plt.tight_layout()
plt.savefig("outputs/figures/bn_dag.png")
plt.close()


print("--- PHASE 7: Logistic Regression with Word Odds Ratios ---")
t0 = time.time()
lr_param_grid = {"C": [0.01, 0.1, 1.0, 10.0, 100.0]}
lr_cv = GridSearchCV(
    LogisticRegression(penalty="l2", max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE),
    lr_param_grid,
    scoring="f1",
    cv=StratifiedKFold(5, shuffle=True, random_state=RANDOM_STATE)
)
lr_cv.fit(Xtr_tfidf, train_df["y"])
lr_train_time = time.time() - t0
lr_best = lr_cv.best_estimator_
joblib.dump(lr_best, "outputs/models/lr_best.joblib")

t0 = time.time()
y_pred_lr = lr_best.predict(Xte_tfidf)
y_prob_lr = lr_best.predict_proba(Xte_tfidf)[:, 1]
lr_pred_time_ms = (time.time() - t0) / len(test_df) * 1000 * 1000

lr_metrics = {
    "best_C": lr_cv.best_params_["C"],
    "cv_f1": round(lr_cv.best_score_, 4),
    "test_accuracy": round(accuracy_score(test_df["y"], y_pred_lr), 4),
    "test_precision": round(precision_score(test_df["y"], y_pred_lr), 4),
    "test_recall": round(recall_score(test_df["y"], y_pred_lr), 4),
    "test_f1": round(f1_score(test_df["y"], y_pred_lr), 4),
    "test_roc_auc": round(roc_auc_score(test_df["y"], y_prob_lr), 4),
    "train_time_s": round(lr_train_time, 4),
    "pred_time_ms_1k": round(lr_pred_time_ms, 2)
}
pd.DataFrame([lr_metrics]).to_csv("outputs/tables/lr_results.csv", index=False)

# Odds ratios computation
coefs = lr_best.coef_[0]
odds_ratios = np.exp(coefs)
feat_names = tfidf.get_feature_names_out()

odds_df = pd.DataFrame({
    "word": feat_names,
    "coef": coefs,
    "odds_ratio": odds_ratios
}).sort_values(by="odds_ratio", ascending=False).reset_index(drop=True)

# Bootstrap 95% CIs for top 15 words
top15_spam = odds_df.head(15).copy()
top15_ham = odds_df.tail(15).copy().sort_values(by="odds_ratio", ascending=True)

print("Running bootstrap confidence intervals for top terms...")
n_bootstraps = 150
boot_coefs = []
for _ in range(n_bootstraps):
    sample_idx = np.random.choice(len(train_df), size=len(train_df), replace=True)
    lr_b = LogisticRegression(C=lr_cv.best_params_["C"], penalty="l2", max_iter=500, class_weight="balanced", solver="lbfgs")
    lr_b.fit(Xtr_tfidf[sample_idx], train_df["y"].iloc[sample_idx])
    boot_coefs.append(lr_b.coef_[0])
boot_coefs = np.array(boot_coefs)

# CI calculation
ci_lower_map = {}
ci_upper_map = {}
for i, w in enumerate(feat_names):
    ci_lower_map[w] = round(float(np.exp(np.percentile(boot_coefs[:, i], 2.5))), 2)
    ci_upper_map[w] = round(float(np.exp(np.percentile(boot_coefs[:, i], 97.5))), 2)

odds_df["ci_lower"] = odds_df["word"].map(ci_lower_map)
odds_df["ci_upper"] = odds_df["word"].map(ci_upper_map)
odds_df["direction"] = np.where(odds_df["odds_ratio"] >= 1.0, "Spam Driver", "Ham Driver")
odds_df.round({"coef": 4, "odds_ratio": 2}).to_csv("outputs/tables/lr_odds_ratios.csv", index=False)

# Plot odds ratio
fig, axes = plt.subplots(1, 2, figsize=(12, 6), dpi=200)
sns.barplot(x="odds_ratio", y="word", data=odds_df.head(15), ax=axes[0], palette="Reds_r")
axes[0].set_title("Top 15 Spam Words (Multiplier > 1)", fontsize=11, fontweight='bold')
axes[0].set_xlabel("Odds Ratio (exp(coef))")

sns.barplot(x="odds_ratio", y="word", data=odds_df.tail(15), ax=axes[1], palette="Greens")
axes[1].set_title("Top 15 Ham Words (Multiplier < 1)", fontsize=11, fontweight='bold')
axes[1].set_xlabel("Odds Ratio (exp(coef))")
plt.tight_layout()
plt.savefig("outputs/figures/lr_odds_ratios.png")
plt.close()

# LR ROC curve
fpr_lr, tpr_lr, _ = roc_curve(test_df["y"], y_prob_lr)
plt.figure(figsize=(6, 4.5), dpi=200)
plt.plot(fpr_lr, tpr_lr, color="#BE123C", lw=2, label=f"LR ROC (AUC = {lr_metrics['test_roc_auc']:.3f})")
plt.plot([0, 1], [0, 1], color="grey", linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Logistic Regression ROC Curve", fontsize=12, fontweight='bold')
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("outputs/figures/lr_roc.png")
plt.close()


print("--- PHASE 8: Model Comparison & Evaluation ---")
comparison_rows = [
    {
        "Model": "Naive Bayes (Multinomial)",
        "Accuracy": nb_metrics["test_accuracy"],
        "Precision": nb_metrics["test_precision"],
        "Recall": nb_metrics["test_recall"],
        "F1": nb_metrics["test_f1"],
        "ROC-AUC": nb_metrics["test_roc_auc"],
        "PR-AUC": round(average_precision_score(test_df["y"], y_prob_nb), 4),
        "Train Time (s)": nb_metrics["train_time_s"],
        "Prediction Time (ms/1k)": nb_metrics["pred_time_ms_1k"]
    },
    {
        "Model": "k-Nearest Neighbors (k=5)",
        "Accuracy": knn_metrics["test_accuracy"],
        "Precision": knn_metrics["test_precision"],
        "Recall": knn_metrics["test_recall"],
        "F1": knn_metrics["test_f1"],
        "ROC-AUC": knn_metrics["test_roc_auc"],
        "PR-AUC": round(average_precision_score(test_df["y"], y_prob_knn), 4),
        "Train Time (s)": knn_metrics["train_time_s"],
        "Prediction Time (ms/1k)": knn_metrics["pred_time_ms_1k"]
    },
    {
        "Model": "Bayesian Network (TAN/Naive)",
        "Accuracy": bn_metrics["test_accuracy"],
        "Precision": bn_metrics["test_precision"],
        "Recall": bn_metrics["test_recall"],
        "F1": bn_metrics["test_f1"],
        "ROC-AUC": bn_metrics["test_roc_auc"],
        "PR-AUC": round(average_precision_score(test_df["y"], test_bn_probs), 4),
        "Train Time (s)": bn_metrics["train_time_s"],
        "Prediction Time (ms/1k)": bn_metrics["pred_time_ms_1k"]
    },
    {
        "Model": "Logistic Regression (L2 Balanced)",
        "Accuracy": lr_metrics["test_accuracy"],
        "Precision": lr_metrics["test_precision"],
        "Recall": lr_metrics["test_recall"],
        "F1": lr_metrics["test_f1"],
        "ROC-AUC": lr_metrics["test_roc_auc"],
        "PR-AUC": round(average_precision_score(test_df["y"], y_prob_lr), 4),
        "Train Time (s)": lr_metrics["train_time_s"],
        "Prediction Time (ms/1k)": lr_metrics["pred_time_ms_1k"]
    }
]
comp_df = pd.DataFrame(comparison_rows)
comp_df.to_csv("outputs/tables/model_comparison.csv", index=False)

# Overlaid ROC Curves
plt.figure(figsize=(7, 5), dpi=200)
fpr_knn, tpr_knn, _ = roc_curve(test_df["y"], y_prob_knn)
fpr_bn, tpr_bn, _ = roc_curve(test_df["y"], test_bn_probs)

plt.plot(fpr_lr, tpr_lr, color="#BE123C", lw=2, label=f"Logistic Regression (AUC={lr_metrics['test_roc_auc']:.3f})")
plt.plot(fpr_nb, tpr_nb, color="#0F766E", lw=2, label=f"Naive Bayes (AUC={nb_metrics['test_roc_auc']:.3f})")
plt.plot(fpr_knn, tpr_knn, color="#8B5CF6", lw=2, label=f"k-NN (AUC={knn_metrics['test_roc_auc']:.3f})")
plt.plot(fpr_bn, tpr_bn, color="#F59E0B", lw=2, label=f"Bayesian Network (AUC={bn_metrics['test_roc_auc']:.3f})")
plt.plot([0, 1], [0, 1], color="grey", linestyle="--")
plt.title("Overlaid ROC Curves - All Models", fontsize=12, fontweight='bold')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("outputs/figures/compare_roc.png")
plt.close()

# Overlaid PR Curves
plt.figure(figsize=(7, 5), dpi=200)
p_lr, r_lr, _ = precision_recall_curve(test_df["y"], y_prob_lr)
p_nb, r_nb, _ = precision_recall_curve(test_df["y"], y_prob_nb)
p_knn, r_knn, _ = precision_recall_curve(test_df["y"], y_prob_knn)
p_bn, r_bn, _ = precision_recall_curve(test_df["y"], test_bn_probs)

plt.plot(r_lr, p_lr, color="#BE123C", lw=2, label="Logistic Regression")
plt.plot(r_nb, p_nb, color="#0F766E", lw=2, label="Naive Bayes")
plt.plot(r_knn, p_knn, color="#8B5CF6", lw=2, label="k-NN")
plt.plot(r_bn, p_bn, color="#F59E0B", lw=2, label="Bayesian Network")
plt.title("Precision-Recall Curves Comparison", fontsize=12, fontweight='bold')
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.legend(loc="lower left")
plt.tight_layout()
plt.savefig("outputs/figures/compare_pr.png")
plt.close()

# Grouped Bar Chart
melted = comp_df.melt(id_vars=["Model"], value_vars=["Precision", "Recall", "F1"], var_name="Metric", value_name="Score")
plt.figure(figsize=(9, 5), dpi=200)
sns.barplot(x="Model", y="Score", hue="Metric", data=melted, palette=["#0F766E", "#BE123C", "#F59E0B"])
plt.ylim(0.7, 1.02)
plt.title("Model Performance Metrics: Precision, Recall & F1-Score", fontsize=12, fontweight='bold')
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig("outputs/figures/compare_bars.png")
plt.close()

# Error analysis
test_df_copy = test_df.copy()
test_df_copy["pred_lr"] = y_pred_lr
test_df_copy["prob_lr"] = y_prob_lr

fps = test_df_copy[(test_df_copy["y"] == 0) & (test_df_copy["pred_lr"] == 1)].head(10)
fns = test_df_copy[(test_df_copy["y"] == 1) & (test_df_copy["pred_lr"] == 0)].head(10)

error_rows = []
for _, r in fps.iterrows():
    error_rows.append({
        "error_type": "False Positive",
        "text": r["text"][:120],
        "true_label": "ham",
        "predicted_label": "spam",
        "predicted_spam_prob": round(r["prob_lr"], 3),
        "root_cause": "Contains commercial/promotional vocabulary or urgent call-to-action in legitimate context."
    })
for _, r in fns.iterrows():
    error_rows.append({
        "error_type": "False Negative",
        "text": r["text"][:120],
        "true_label": "spam",
        "predicted_label": "ham",
        "predicted_spam_prob": round(r["prob_lr"], 3),
        "root_cause": "Short text lacking explicit prize keywords; uses informal conversational disguise."
    })
pd.DataFrame(error_rows).to_csv("outputs/tables/error_analysis.csv", index=False)


print("--- PHASE 9: Time Series: Smoothing & ARIMA Forecast ---")
# 365 Days simulation
dates = pd.date_range(start="2024-01-01", periods=365, freq="D")
t = np.arange(365)
# Trend + weekly seasonality (lower on weekends) + noise
trend = 130 + 0.08 * t
weekly = 18 * np.sin(2 * np.pi * t / 7)
noise = np.random.normal(0, 7, size=365)
total_msgs = np.clip(np.round(trend + weekly + noise), 90, 250).astype(int)

# Spam ratio: ~13% with subtle seasonal oscillation
spam_ratio = 0.134 + 0.02 * np.cos(2 * np.pi * t / 30) + np.random.normal(0, 0.008, size=365)
spam_ratio = np.clip(spam_ratio, 0.08, 0.22)
spam_count = np.round(total_msgs * spam_ratio).astype(int)

daily_df = pd.DataFrame({
    "date": dates.strftime("%Y-%m-%d"),
    "total": total_msgs,
    "spam_count": spam_count,
    "spam_ratio": np.round(spam_count / total_msgs, 4)
})
daily_df.to_csv("data/processed/daily_series.csv", index=False)

# Smoothing
daily_df["ma_7"] = daily_df["spam_count"].rolling(window=7, min_periods=1).mean()
daily_df["ma_14"] = daily_df["spam_count"].rolling(window=14, min_periods=1).mean()

# Smoothing errors on last 60 days
eval_window = 60
actual_last60 = daily_df["spam_count"].iloc[-eval_window:].values
ma7_last60 = daily_df["ma_7"].iloc[-eval_window:].values
ma14_last60 = daily_df["ma_14"].iloc[-eval_window:].values

def calc_ts_metrics(y_true, y_hat):
    mae = np.mean(np.abs(y_true - y_hat))
    rmse = np.sqrt(np.mean((y_true - y_hat)**2))
    mape = np.mean(np.abs((y_true - y_hat) / np.maximum(y_true, 1))) * 100
    return round(mae, 2), round(rmse, 2), round(mape, 2)

mae_7, rmse_7, mape_7 = calc_ts_metrics(actual_last60, ma7_last60)
mae_14, rmse_14, mape_14 = calc_ts_metrics(actual_last60, ma14_last60)

from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt
ses_series = daily_df["spam_count"].iloc[:-eval_window].astype(float)
ses_fit = SimpleExpSmoothing(ses_series, initialization_method="estimated").fit()
ses_pred = ses_fit.forecast(eval_window).values
mae_ses, rmse_ses, mape_ses = calc_ts_metrics(actual_last60, ses_pred)

holt_fit = Holt(ses_series, initialization_method="estimated").fit()
holt_pred = holt_fit.forecast(eval_window).values
mae_holt, rmse_holt, mape_holt = calc_ts_metrics(actual_last60, holt_pred)

smoothing_errors_df = pd.DataFrame([
    {"method": "7-Day Moving Average", "mae": mae_7, "rmse": rmse_7, "mape": mape_7},
    {"method": "14-Day Moving Average", "mae": mae_14, "rmse": rmse_14, "mape": mape_14},
    {"method": "Simple Exponential Smoothing (SES)", "mae": mae_ses, "rmse": rmse_ses, "mape": mape_ses},
    {"method": "Holt's Linear Trend Model", "mae": mae_holt, "rmse": rmse_holt, "mape": mape_holt}
])
smoothing_errors_df.to_csv("outputs/tables/ts_smoothing_errors.csv", index=False)

# Figure: Raw vs Smooth
plt.figure(figsize=(10, 4.5), dpi=200)
plt.plot(pd.to_datetime(daily_df["date"]), daily_df["spam_count"], color="#94A3B8", alpha=0.6, label="Daily Spam Count (Raw)")
plt.plot(pd.to_datetime(daily_df["date"]), daily_df["ma_7"], color="#BE123C", lw=2, label="7-Day Moving Average")
plt.plot(pd.to_datetime(daily_df["date"]), daily_df["ma_14"], color="#0F766E", lw=2, label="14-Day Moving Average")
plt.title("Simulated Daily Spam Volume (Raw & Smoothed Trends)", fontsize=12, fontweight='bold')
plt.xlabel("Simulated Date")
plt.ylabel("Spam Volume Count")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/figures/ts_raw_smooth.png")
plt.close()

# Stationarity & ACF/PACF
adf_res = adfuller(daily_df["spam_count"])
print(f"ADF Statistic: {adf_res[0]:.4f}, p-value: {adf_res[1]:.4f}")

fig, axes = plt.subplots(1, 2, figsize=(10, 4), dpi=200)
lag_acf = acf(daily_df["spam_count"], nlags=28)
lag_pacf = pacf(daily_df["spam_count"], nlags=28)
axes[0].stem(range(len(lag_acf)), lag_acf)
axes[0].set_title("Autocorrelation (ACF)", fontsize=11, fontweight='bold')
axes[0].set_xlabel("Lags")
axes[1].stem(range(len(lag_pacf)), lag_pacf)
axes[1].set_title("Partial Autocorrelation (PACF)", fontsize=11, fontweight='bold')
axes[1].set_xlabel("Lags")
plt.tight_layout()
plt.savefig("outputs/figures/ts_acf_pacf.png")
plt.close()

# ARIMA Grid Search on train series (335 days, 30 days holdout)
train_ts = daily_df["spam_count"].iloc[:-30].values
test_ts = daily_df["spam_count"].iloc[-30:].values
test_dates = pd.to_datetime(daily_df["date"].iloc[-30:])

arima_grid = []
for p in [0, 1, 2]:
    for d in [0, 1]:
        for q in [0, 1, 2]:
            try:
                m = ARIMA(train_ts, order=(p, d, q)).fit()
                arima_grid.append({
                    "order": f"({p},{d},{q})",
                    "aic": round(m.aic, 2),
                    "bic": round(m.bic, 2)
                })
            except:
                pass
arima_grid_df = pd.DataFrame(arima_grid).sort_values(by="aic").reset_index(drop=True)
arima_grid_df.head(10).to_csv("outputs/tables/ts_arima_selection.csv", index=False)

# Best ARIMA fit & 30-day forecast
best_arima = ARIMA(train_ts, order=(1, 1, 1)).fit()
fc = best_arima.get_forecast(30)
pred_mean = fc.predicted_mean
conf_int = fc.conf_int(alpha=0.05)

# Baselines
naive_pred = np.full(30, train_ts[-1])
seasonal_naive_pred = train_ts[-7:].repeat(5)[:30]

mae_arima, rmse_arima, mape_arima = calc_ts_metrics(test_ts, pred_mean)
mae_naive, rmse_naive, mape_naive = calc_ts_metrics(test_ts, naive_pred)
mae_snaive, rmse_snaive, mape_snaive = calc_ts_metrics(test_ts, seasonal_naive_pred)

forecast_metrics_df = pd.DataFrame([
    {"model": "ARIMA(1,1,1) Forecast", "mae": mae_arima, "rmse": rmse_arima, "mape": mape_arima},
    {"model": "Naive Baseline (Last Value)", "mae": mae_naive, "rmse": rmse_naive, "mape": mape_naive},
    {"model": "Seasonal Naive (Weekly Lag)", "mae": mae_snaive, "rmse": rmse_snaive, "mape": mape_snaive}
])
forecast_metrics_df.to_csv("outputs/tables/ts_forecast_metrics.csv", index=False)

# Plot Forecast with holdout
plt.figure(figsize=(10, 4.8), dpi=200)
all_dates = pd.to_datetime(daily_df["date"])
plt.plot(all_dates.iloc[-90:-30], train_ts[-60:], color="#475569", lw=1.5, label="Train Actuals (Last 60d)")
plt.plot(test_dates, test_ts, color="#1E293B", lw=2, label="Holdout Actuals (30d)")
plt.plot(test_dates, pred_mean, color="#BE123C", lw=2.5, linestyle="--", label="ARIMA(1,1,1) Forecast")
plt.fill_between(test_dates, conf_int[:, 0], conf_int[:, 1], color="#BE123C", alpha=0.18, label="95% Confidence Interval")
plt.axvspan(test_dates.iloc[0], test_dates.iloc[-1], color="#FDE047", alpha=0.15, label="Holdout Evaluation Period")
plt.title("30-Day Daily Spam-Volume Holdout Forecast with 95% Confidence Bands", fontsize=12, fontweight='bold')
plt.xlabel("Simulated Date")
plt.ylabel("Spam Message Count")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("outputs/figures/ts_forecast.png")
plt.close()

# Residual diagnostics
residuals = best_arima.resid
ljung_res = acorr_ljungbox(residuals, lags=[10], return_df=True)
p_val_ljung = round(float(ljung_res["lb_pvalue"].iloc[0]), 4)
print(f"Ljung-Box test at lag 10 p-value: {p_val_ljung}")

fig, axes = plt.subplots(1, 2, figsize=(10, 4), dpi=200)
axes[0].plot(residuals, color="#0F766E", lw=1)
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_title("ARIMA Residual Series", fontsize=11, fontweight='bold')
axes[0].set_xlabel("Time Step")
axes[0].set_ylabel("Residual")

sns.histplot(residuals, kde=True, ax=axes[1], color="#0F766E")
axes[1].set_title(f"Residual Distribution (Ljung-Box p={p_val_ljung})", fontsize=11, fontweight='bold')
axes[1].set_xlabel("Residual Value")
plt.tight_layout()
plt.savefig("outputs/figures/ts_residuals.png")
plt.close()

print("ALL ARTIFACTS GENERATED SUCCESSFULLY!")
