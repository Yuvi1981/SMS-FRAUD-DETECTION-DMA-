import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"D:\DMA"
TEMPLATE_PATH = os.path.join(BASE_DIR, "report", "DMA_Mini_Project_Report_Template.docx")
OUTPUT_DOCX = os.path.join(BASE_DIR, "report", "DMA_Mini_Project_Report_Filled.docx")
OUTPUT_PDF = os.path.join(BASE_DIR, "report", "DMA_Mini_Project_Report_Filled.pdf")

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_cell(cell, text, bold=False, italic=False, font_size=8.0, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.02
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.bold = bold
        r.italic = italic
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=50, bottom=50, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text, space_before=4, space_after=1.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text, space_before=3, space_after=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.bold = True
    r.font.color.rgb = RGBColor(20, 20, 20)
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=2.0, font_size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(font_size)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(font_size)
    return p

def add_bullet_p(doc, bold_prefix, text, space_after=1.5, font_size=9.0):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.04
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_bullet = p.add_run("• ")
    r_bullet.font.name = "Times New Roman"
    r_bullet.font.size = Pt(font_size)
    r_bullet.bold = True
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(font_size)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(font_size)
    return p

def add_caption(doc, text, space_before=1.5, space_after=1.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.5)
    r.bold = True
    r.italic = True
    return p

def add_interpretation(doc, text, space_after=2.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.04
    r_pre = p.add_run("Interpretation: ")
    r_pre.font.name = "Times New Roman"
    r_pre.font.size = Pt(8.5)
    r_pre.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.5)
    return p

def add_figure(doc, img_rel_path, width_inches, caption_text, interp_text=None):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(2)
    p_img.paragraph_format.space_after = Pt(1.5)
    p_img.paragraph_format.keep_with_next = True
    full_path = os.path.join(BASE_DIR, img_rel_path)
    if os.path.exists(full_path):
        run = p_img.add_run()
        run.add_picture(full_path, width=Inches(width_inches))
    else:
        p_img.add_run(f"[Image file not found: {img_rel_path}]")
    add_caption(doc, caption_text)
    if interp_text:
        add_interpretation(doc, interp_text)

def add_code_snippet(doc, snippet_title, code_lines):
    add_heading_2(doc, snippet_title, space_before=2.5, space_after=1)
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    format_cell(cell, "\n".join(code_lines), font_size=7.5, bg_color="F7F7FA")
    set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
    p = cell.paragraphs[0]
    for r in p.runs:
        r.font.name = "Consolas"
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(2)

print("Opening template document...")
doc = Document(TEMPLATE_PATH)

# Verify template paragraphs (Cover = Page 1, Index = Page 2)
print(f"Template contains {len(doc.paragraphs)} paragraphs.")

# Add page break after Page 2 (index)
p_last_idx = doc.paragraphs[-1]
p_last_idx.paragraph_format.space_after = Pt(0)
doc.add_page_break()

# =============================================================================
# PAGE 3: SECTIONS 1 TO 5
# =============================================================================
print("Writing Page 3 (Sections 1 to 5)...")
add_heading_1(doc, "1. Title", space_before=0, space_after=1.5)
add_body_p(doc, "End-to-End SMS Spam Classification and Volume Forecasting Using Probabilistic and Supervised Machine Learning Architectures with Logistic Odds Ratio Interpretability", font_size=9.5)

add_heading_1(doc, "2. Abstract", space_before=3, space_after=1.5)
abstract_text = (
    "The rapid proliferation of unsolicited and fraudulent Short Message Service (SMS) communications poses significant security, privacy, and economic challenges for mobile telecommunications infrastructure. "
    "In this project, a comprehensive data mining and analytics pipeline was developed to accurately classify SMS messages and project temporal transmission volumes. The study evaluated the benchmark UCI SMS Spam Collection, "
    "comprising 5,169 deduplicated messages exhibiting an imbalanced distribution of 87.37% legitimate messages (4,516 ham) and 12.63% spam messages (653 spam). A robust preprocessing pipeline encompassing regex entity masking, "
    "tokenization, stopword removal, and Porter stemming was applied prior to TF-IDF n-gram vectorization and Chi-square feature selection. Four predictive architectures were benchmarked on a stratified 20% holdout test set (1,034 messages): "
    "Multinomial Naive Bayes, k-Nearest Neighbors (k=5), a Tree-Augmented / Naive Bayesian Network, and L2-regularized Logistic Regression. Logistic Regression emerged as the champion model, achieving a test F1-score of 0.9653, "
    "an accuracy of 0.9913, an ROC-AUC of 0.9971, and an inference latency of 1.18 ms per 1,000 queries. Furthermore, an ARIMA(1,1,1) model fitted on 365 daily volume counts achieved a Mean Absolute Percentage Error of 12.11% on a 30-day forecast."
)
add_body_p(doc, abstract_text, font_size=9.0)

add_heading_1(doc, "3. Introduction", space_before=3, space_after=1.5)
add_body_p(
    doc,
    "Short Message Service (SMS) remains one of the most widely used direct communication channels globally, with open rates exceeding 95%. "
    "However, this ubiquitous adoption makes it a lucrative target for smishing, financial scams, lottery hoaxes, and predatory promotions. "
    "Static keyword filters are brittle and easily circumvented by adversarial typos, making statistical text mining and machine learning indispensable.",
    font_size=9.0
)
add_body_p(
    doc,
    "Text mining transforms unstructured text into structured numerical feature spaces through normalization, tokenization, n-gram extraction, and frequency weighting. "
    "This project builds an audited, end-to-end data mining pipeline addressing class-imbalanced text classification, empirical odds ratio interpretability, and daily traffic forecasting.",
    font_size=9.0
)

add_heading_1(doc, "4. Problem Statement", space_before=3, space_after=1.5)
add_body_p(
    doc,
    "Given the severe 87:13 class imbalance in mobile communications and the 160-character constraint of SMS messages, classifiers face the dual challenge of eliminating false positives on personal messages while maintaining high recall on deceptive spam. "
    "This project develops an accurate, interpretable, and computationally efficient classification and temporal forecasting system capable of reliably filtering spam while forecasting transmission volumes for telecom capacity planning.",
    font_size=9.0
)

add_heading_1(doc, "5. Objectives", space_before=3, space_after=1.5)
add_bullet_p(doc, "1. Corpus Auditing: ", "Acquire, clean, and deduplicate the UCI SMS Spam Collection, establishing an audited baseline of 5,169 messages with zero data leakage.", font_size=8.8)
add_bullet_p(doc, "2. Exploratory Profiling: ", "Quantify message lengths, entity distributions (URLs, phone numbers, currency), and lexical patterns across spam and ham classes.", font_size=8.8)
add_bullet_p(doc, "3. Feature Engineering: ", "Develop regex entity masking (urltoken, phonetoken, moneytoken, numtoken) and Porter stemming to capture discriminatory morphological signatures.", font_size=8.8)
add_bullet_p(doc, "4. Statistical Feature Selection: ", "Extract unigram/bigram TF-IDF representations and isolate the top 500 features using Chi-square (χ²) independence tests.", font_size=8.8)
add_bullet_p(doc, "5. Cross-Model Benchmarking: ", "Train and evaluate Naive Bayes, k-NN, Bayesian Network, and Logistic Regression on a strict stratified 20% holdout split.", font_size=8.8)
add_bullet_p(doc, "6. Interpretability & Forecasting: ", "Extract exact word-level odds ratios (exp(β)) for transparent auditing, and model 365-day message trajectories using ARIMA time-series forecasting.", font_size=8.8)

doc.add_page_break()

# =============================================================================
# PAGE 4: SECTIONS 6 & 7
# =============================================================================
print("Writing Page 4 (Sections 6 and 7)...")
add_heading_1(doc, "6. Data set and Libraries required", space_before=0, space_after=1.5)
add_body_p(
    doc,
    "The experimental evaluation was conducted on the benchmark UCI SMS Spam Collection. Deduplication of the 5,572 raw records removed 403 redundant entries, "
    "yielding an audited corpus of 5,169 unique SMS messages (4,516 ham [87.37%] and 653 spam [12.63%]). Spam messages average 138.1 characters and 23.7 words, "
    "compared to 71.0 characters and 14.2 words for legitimate messages. Moreover, spam exhibits heavy concentrations of digits (94.03%), phone numbers (51.61%), "
    "currency/prize terms (41.65%), and hyperlinks (13.78%), whereas ham messages almost entirely lack external links (0.02%) and phone contacts (0.07%).",
    font_size=9.0
)

add_caption(doc, "Table 1: Corpus Summary Statistics (Outputs from eda_summary.csv)")
t1 = doc.add_table(rows=4, cols=10)
set_table_borders(t1)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER

headers1 = ["Class", "Count", "Share (%)", "Avg Chars", "Avg Words", "Digits (%)", "URL (%)", "Money (%)", "Phone (%)", "Caps Words"]
for c_idx, h in enumerate(headers1):
    format_cell(t1.rows[0].cells[c_idx], h, bold=True, font_size=7.5, bg_color="E6E6EF", align=WD_ALIGN_PARAGRAPH.CENTER)

rows1_data = [
    ["Ham", "4,516", "87.37%", "71.0", "14.2", "15.81%", "0.02%", "2.55%", "0.07%", "0.45"],
    ["Spam", "653", "12.63%", "138.1", "23.7", "94.03%", "13.78%", "41.65%", "51.61%", "2.69"],
    ["Total", "5,169", "100.0%", "79.5", "15.4", "25.69%", "1.76%", "7.49%", "6.58%", "0.73"]
]
for r_idx, r_data in enumerate(rows1_data):
    bg = "FAF9FD" if r_idx == 2 else None
    for c_idx, val in enumerate(r_data):
        align = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        format_cell(t1.rows[r_idx+1].cells[c_idx], val, bold=(r_idx==2), font_size=7.5, bg_color=bg, align=align)

add_interpretation(doc, "Spam messages exhibit nearly twice the length of legitimate communications and contain overwhelming concentrations of digits, phone numbers, and monetary triggers.")

add_caption(doc, "Table 2: Required Python Libraries, Versions, and Purpose (from requirements.txt)")
t2 = doc.add_table(rows=6, cols=3)
set_table_borders(t2)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_idx, h in enumerate(["Library Name", "Version Specification", "Functional Purpose in Project Pipeline"]):
    format_cell(t2.rows[0].cells[c_idx], h, bold=True, font_size=7.5, bg_color="E6E6EF", align=WD_ALIGN_PARAGRAPH.CENTER)

lib_data = [
    ["scikit-learn", ">= 1.3.0", "TF-IDF vectorization, Chi-square feature selection, Naive Bayes, k-NN, Logistic Regression, StratifiedKFold cross-validation."],
    ["pandas & numpy", ">= 2.0.0 / >= 1.24.0", "Tabular dataset ingestion, text corpus filtering, stratified train/test partitioning, matrix algebra, and log-odds computation."],
    ["nltk", ">= 3.8.0", "Natural language toolkit used for English stopword corpus filtering, word tokenization, and Porter morphological stemming."],
    ["statsmodels", ">= 0.14.0", "Time-series modeling, ARIMA(1,1,1) model estimation, moving average smoothing, and forecast error metric evaluation."],
    ["matplotlib & seaborn", ">= 3.8.0 / >= 0.13.0", "Generation of publication-quality statistical figures, ROC curves, confusion matrices, and forecast confidence bands."]
]
for r_idx, r_data in enumerate(lib_data):
    for c_idx, val in enumerate(r_data):
        format_cell(t2.rows[r_idx+1].cells[c_idx], val, bold=(c_idx==0), font_size=7.5)

add_heading_1(doc, "7. Approach / Methodology", space_before=3, space_after=1.5)
add_body_p(
    doc,
    "The methodology comprises five sequential phases executed under a strict leak-free evaluation protocol:",
    font_size=9.0
)
add_bullet_p(
    doc,
    "Text Normalization & Entity Masking: ",
    "Text was converted to lowercase. Regular expressions masked URLs with 'urltoken', phone numbers (7+ digits) with 'phonetoken', currency/prize terms with 'moneytoken', and numbers with 'numtoken'. Punctuation was stripped, English stopwords removed, and tokens stemmed via Porter stemmer.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Feature Engineering & Chi-Square Selection: ",
    "Unigram and bigram TF-IDF representations (min_df=2) were extracted. Chi-square (χ²) tests identified the top 500 features against class labels. Leading discriminators included numtoken (χ²=6,783.33), phonetoken (χ²=1,939.21), numtoken numtoken (χ²=1,735.07), moneytoken (χ²=1,372.52), call phonetoken (χ²=1,147.02), call (χ²=905.69), free (χ²=791.33), txt (χ²=713.39), claim (χ²=505.27), and prize (χ²=463.74).",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Supervised Classification Architectures: ",
    "Four architectures were implemented: (1) Multinomial Naive Bayes using log-likelihood estimation; (2) k-Nearest Neighbors using distance weighting over TF-IDF space; (3) Bayesian Network utilizing a Directed Acyclic Graph with class root SPAM ∈ {0, 1}; and (4) L2-regularized Logistic Regression with inverse class weighting.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Strict Evaluation Protocol: ",
    "A stratified 80/20 train/test split (Train: 4,135; Test: 1,034 messages) ensured strict partitioning with zero test leakage. All vectorizers and selectors were fitted solely on training data. Metrics evaluated: Accuracy, Precision, Recall, F1-Score, ROC-AUC, PR-AUC, and latency per 1,000 queries.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Time-Series Volume Modeling: ",
    "Daily message trajectories were simulated over a 365-day calendar. 7-day and 14-day rolling moving averages and an ARIMA(1,1,1) model were fitted to forecast volumes over a 30-day out-of-sample holdout test window.",
    font_size=8.8
)

doc.add_page_break()

# =============================================================================
# PAGE 5: SECTION 8 (IMPLEMENTATION)
# =============================================================================
print("Writing Page 5 (Section 8)...")
add_heading_1(doc, "8. Implementation", space_before=0, space_after=1.5)
add_body_p(
    doc,
    "The complete data mining and analytics pipeline was implemented in Python using scikit-learn, statsmodels, and NLTK. Model training and hyperparameter optimization were conducted using 5-fold Stratified Cross-Validation on the 4,135 training samples. "
    "The chosen optimal hyperparameters derived from grid search were: (1) Naive Bayes: Laplace smoothing alpha = 0.1 (yielding CV F1 = 0.9449); (2) k-NN: k = 5 with distance-based weighting (yielding CV F1 = 0.9069); "
    "(3) Logistic Regression: inverse regularization parameter C = 10.0 with balanced class weighting (yielding CV F1 = 0.9377); and (4) Time-Series: ARIMA order (1,1,1) identified via minimum AIC/BIC criteria (AIC = 1558.56, BIC = 1569.99).",
    font_size=9.0
)

add_code_snippet(doc, "Listing 1: Text Preprocessing and Regex Entity Token Substitution", [
    "def clean_and_tokenize(text):",
    "    text = re.sub(r'(https?://\\S+|www\\.\\S+)', ' urltoken ', str(text).lower())",
    "    text = re.sub(r'\\b\\d{7,}\\b', ' phonetoken ', text)",
    "    text = re.sub(r'[\\$£€]\\s?\\d*|prize|claim|cash|won', ' moneytoken ', text)",
    "    text = re.sub(r'\\d+', ' numtoken ', text)",
    "    text = re.sub(r'[^a-z\\s]', ' ', text)",
    "    tokens = [stemmer.stem(w) for w in text.split() if w not in STOP_WORDS and len(w) > 1]",
    "    return ' '.join(tokens) if tokens else 'texttoken'"
])

add_code_snippet(doc, "Listing 2: TF-IDF Representation & Chi-Square Feature Selection", [
    "tfidf = TfidfVectorizer(min_df=2, ngram_range=(1, 2))",
    "X_train_tfidf = tfidf.fit_transform(train_df['tokens'])",
    "X_test_tfidf = tfidf.transform(test_df['tokens'])",
    "chi2_sel = SelectKBest(chi2, k=min(500, X_train_tfidf.shape[1]))",
    "X_train_chi2 = chi2_sel.fit_transform(X_train_tfidf, train_df['y'])",
    "X_test_chi2 = chi2_sel.transform(X_test_tfidf)"
])

add_code_snippet(doc, "Listing 3: Balanced L2-Regularized Logistic Regression Training", [
    "lr_model = LogisticRegression(C=10.0, penalty='l2', solver='lbfgs',",
    "                              class_weight='balanced', max_iter=1000, random_state=42)",
    "lr_model.fit(X_train_tfidf, train_df['y'])",
    "y_pred_lr = lr_model.predict(X_test_tfidf)",
    "y_prob_lr = lr_model.predict_proba(X_test_tfidf)[:, 1]",
    "odds_ratios = np.exp(lr_model.coef_[0])"
])

add_code_snippet(doc, "Listing 4: ARIMA(1,1,1) Daily Message Volume Fitting & 30-Day Forecast", [
    "train_ts = daily_series['spam_count'].iloc[:-30]",
    "test_ts = daily_series['spam_count'].iloc[-30:]",
    "arima_model = ARIMA(train_ts, order=(1, 1, 1)).fit()",
    "forecast_res = arima_model.get_forecast(steps=30)",
    "forecast_mean = forecast_res.predicted_mean",
    "conf_int = forecast_res.conf_int(alpha=0.05)"
])

doc.add_page_break()

# =============================================================================
# PAGE 6: SECTION 9 - PART 1 (CLASSIFIER RESULTS)
# =============================================================================
print("Writing Page 6 (Section 9 Part 1)...")
add_heading_1(doc, "9. Results", space_before=0, space_after=1.5)
add_body_p(
    doc,
    "The predictive performance of all four classification architectures was evaluated on the identical 20% stratified holdout test split (1,034 messages: 131 spam and 903 ham messages). "
    "Table 3 summarizes the exact benchmark metrics extracted from outputs/tables/model_comparison.csv.",
    font_size=9.0
)

add_caption(doc, "Table 3: Cross-Model Benchmark Performance on Test Split (Outputs from model_comparison.csv)")
t3 = doc.add_table(rows=5, cols=9)
set_table_borders(t3)
t3.alignment = WD_TABLE_ALIGNMENT.CENTER

headers3 = ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "PR-AUC", "Train (s)", "Latency (ms/1k)"]
for c_idx, h in enumerate(headers3):
    format_cell(t3.rows[0].cells[c_idx], h, bold=True, font_size=7.5, bg_color="E6E6EF", align=WD_ALIGN_PARAGRAPH.CENTER)

rows3_data = [
    ["Naive Bayes (Multinomial)", "0.9845", "0.9600", "0.9160", "0.9375", "0.9954", "0.9830", "0.3095", "1.64 ms"],
    ["k-Nearest Neighbors (k=5)", "0.9758", "0.9569", "0.8473", "0.8988", "0.9869", "0.9665", "0.0026", "191.13 ms"],
    ["Bayesian Network (TAN/Naive)", "0.9758", "0.9569", "0.8473", "0.8988", "0.9791", "0.9380", "0.0450", "261.57 ms"],
    ["Logistic Regression (L2 Balanced)", "0.9913", "0.9766", "0.9542", "0.9653", "0.9971", "0.9878", "0.9266", "1.18 ms"]
]
for r_idx, r_data in enumerate(rows3_data):
    bg = "EDE9FE" if r_idx == 3 else None
    for c_idx, val in enumerate(r_data):
        align = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        format_cell(t3.rows[r_idx+1].cells[c_idx], val, bold=(r_idx==3), font_size=7.5, bg_color=bg, align=align)

add_interpretation(doc, "Logistic Regression achieved the highest F1-score (0.9653), highest Precision (0.9766), highest Recall (0.9542), and highest ROC-AUC (0.9971), while executing 1,000 inferences in only 1.18 milliseconds (over 160 times faster than k-NN).")

add_figure(
    doc,
    "outputs/figures/compare_roc.png",
    width_inches=3.6,
    caption_text="Figure 1: Cross-Model Receiver Operating Characteristic (ROC) Curves",
    interp_text="Logistic Regression achieved an exceptional ROC-AUC of 0.9971, closely followed by Naive Bayes at 0.9954, demonstrating superior true positive discrimination at near-zero false positive rates."
)

add_figure(
    doc,
    "outputs/figures/nb_confusion.png",
    width_inches=2.4,
    caption_text="Figure 2: Confusion Matrix for Naive Bayes Classifier on Test Set",
    interp_text="The Naive Bayes confusion matrix confirms strong separation, misclassifying only 5 ham messages out of 903 as false positives while successfully catching 120 out of 131 spam messages."
)

doc.add_page_break()

# =============================================================================
# PAGE 7: SECTION 9 - PART 2 (ODDS RATIOS, BAYESIAN NET, TIME SERIES)
# =============================================================================
print("Writing Page 7 (Section 9 Part 2)...")
add_heading_2(doc, "Word-Level Odds Ratio Interpretability (Logistic Regression)", space_before=0, space_after=1)
add_body_p(
    doc,
    "Logistic regression provides direct mathematical interpretability via word odds ratios, defined as exp(β). "
    "A token with an odds ratio substantially greater than 1.0 sharply multiplies the odds of spam, whereas an odds ratio below 1.0 lowers spam risk. "
    "Table 4 presents the top 10 spam drivers and top 10 ham drivers extracted from outputs/tables/lr_odds_ratios.csv.",
    font_size=8.5
)

add_caption(doc, "Table 4: Top 10 Spam and Ham Drivers by Odds Ratio (Outputs from lr_odds_ratios.csv)")
t4 = doc.add_table(rows=11, cols=6)
set_table_borders(t4)
t4.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_idx, h in enumerate(["Token (Word)", "Beta (β)", "Odds Ratio (e^β)", "95% CI Range", "Impact Direction", "Category"]):
    format_cell(t4.rows[0].cells[c_idx], h, bold=True, font_size=7.0, bg_color="E6E6EF", align=WD_ALIGN_PARAGRAPH.CENTER)

odds_table_data = [
    ["phonetoken", "+13.1479", "512,955.24x", "[60472.1, 560736.9]", "Multiplies Spam Odds", "Spam Driver"],
    ["urltoken", "+10.2910", "29,465.32x", "[1187.1, 53729.2]", "Multiplies Spam Odds", "Spam Driver"],
    ["moneytoken", "+9.1303", "9,231.08x", "[1833.9, 40481.5]", "Multiplies Spam Odds", "Spam Driver"],
    ["numtoken", "+8.1392", "3,426.21x", "[251.5, 40991.6]", "Multiplies Spam Odds", "Spam Driver"],
    ["call phonetoken", "+7.4686", "1,752.18x", "[479.8, 2647.8]", "Multiplies Spam Odds", "Spam Driver"],
    ["txt", "+6.8952", "987.53x", "[151.3, 2310.7]", "Multiplies Spam Odds", "Spam Driver"],
    ["repli", "+6.2014", "493.43x", "[112.3, 1734.3]", "Multiplies Spam Odds", "Spam Driver"],
    ["free", "+4.8192", "123.86x", "[26.7, 1160.8]", "Multiplies Spam Odds", "Spam Driver"],
    ["ok", "-3.1533", "0.04x", "[0.03, 0.16]", "Reduces Spam Odds", "Ham Driver"],
    ["home", "-2.3688", "0.09x", "[0.08, 0.21]", "Reduces Spam Odds", "Ham Driver"]
]
for r_idx, r_data in enumerate(odds_table_data):
    bg = "FEF2F2" if "Spam" in r_data[5] else "F0FDF4"
    for c_idx, val in enumerate(r_data):
        format_cell(t4.rows[r_idx+1].cells[c_idx], val, bold=(c_idx==0), font_size=7.0, bg_color=bg)

add_interpretation(doc, "Engineered entity tokens (phonetoken, urltoken, moneytoken) represent the strongest predictors of spam, multiplying spam odds by factors exceeding 9,000x, while everyday conversational tokens (ok, home) reduce spam odds to 0.04x–0.09x.")

add_figure(
    doc,
    "outputs/figures/bn_dag.png",
    width_inches=2.4,
    caption_text="Figure 3: Bayesian Network Directed Acyclic Graph (DAG) Topology",
    interp_text=None
)

add_caption(doc, "Table 5: Exact Bayesian Posterior Belief Updating (Outputs from bn_example_inferences.csv)")
t5 = doc.add_table(rows=5, cols=4)
set_table_borders(t5)
t5.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_idx, h in enumerate(["Inference Scenario", "Active Observed Evidence", "P(Spam | Evidence)", "P(Ham | Evidence)"]):
    format_cell(t5.rows[0].cells[c_idx], h, bold=True, font_size=7.0, bg_color="E6E6EF", align=WD_ALIGN_PARAGRAPH.CENTER)

bn_inferences = [
    ["Baseline Prior", "No evidence observed (prior dataset baseline)", "12.64%", "87.36%"],
    ["Urgent Financial Bait", "has_money=1, free=1, claim=1", "100.00%", "0.00%"],
    ["Web Link + CTA", "has_url=1, call=1, txt=1", "100.00%", "0.00%"],
    ["Clean Conversational SMS", "All spam trigger tokens absent (= 0)", "0.03%", "99.97%"]
]
for r_idx, r_data in enumerate(bn_inferences):
    for c_idx, val in enumerate(r_data):
        format_cell(t5.rows[r_idx+1].cells[c_idx], val, bold=(c_idx==0), font_size=7.0)

add_figure(
    doc,
    "outputs/figures/ts_forecast.png",
    width_inches=3.0,
    caption_text="Figure 4: 30-Day Holdout Volume Forecast using ARIMA(1,1,1) with 95% Confidence Band",
    interp_text=None
)

add_caption(doc, "Table 6: Time-Series Holdout Forecast and Smoothing Error Evaluation")
t6 = doc.add_table(rows=6, cols=4)
set_table_borders(t6)
t6.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_idx, h in enumerate(["Forecasting / Smoothing Model", "MAE", "RMSE", "MAPE (%)"]):
    format_cell(t6.rows[0].cells[c_idx], h, bold=True, font_size=7.0, bg_color="E6E6EF", align=WD_ALIGN_PARAGRAPH.CENTER)

ts_metrics_data = [
    ["7-Day Moving Average (Smoothing)", "2.13", "2.56", "10.69%"],
    ["14-Day Moving Average (Smoothing)", "2.72", "3.27", "13.54%"],
    ["ARIMA(1,1,1) 30-Day Forecast", "2.48", "2.98", "12.11%"],
    ["Naive Baseline (Last Value)", "2.83", "3.49", "13.05%"],
    ["Seasonal Naive (Weekly Lag)", "4.57", "5.35", "23.80%"]
]
for r_idx, r_data in enumerate(ts_metrics_data):
    bg = "EDE9FE" if r_idx == 2 else None
    for c_idx, val in enumerate(r_data):
        format_cell(t6.rows[r_idx+1].cells[c_idx], val, bold=(r_idx==2), font_size=7.0, bg_color=bg)

add_interpretation(doc, "ARIMA(1,1,1) achieves an out-of-sample forecast MAPE of 12.11%, substantially outperforming the seasonal naive baseline (23.80% MAPE), demonstrating robust capacity for gateway capacity planning.")

doc.add_page_break()

# =============================================================================
# PAGE 8: SECTION 10 (CONCLUSION)
# =============================================================================
print("Writing Page 8 (Section 10)...")
add_heading_1(doc, "10. Conclusion", space_before=0, space_after=1.5)
add_heading_2(doc, "Champion Model Selection Rationale", space_before=2, space_after=1)
add_body_p(
    doc,
    "Across extensive empirical benchmarking on the stratified test split, L2-regularized Logistic Regression with inverse class weighting emerged as the champion classifier. "
    "It demonstrated superior overall performance across all primary metrics: test accuracy of 0.9913, precision of 0.9766, recall of 0.9542, F1-score of 0.9653, "
    "and an ROC-AUC of 0.9971. Crucially, Logistic Regression executed 1,000 message classifications in just 1.18 milliseconds, outperforming k-Nearest Neighbors (191.13 ms) "
    "and Bayesian Network inference (261.57 ms) by over two orders of magnitude. Furthermore, its direct mathematical equivalence to word-level odds ratios (exp(β)) provides "
    "complete transparency and regulatory compliance for telecommunication auditing.",
    font_size=9.0
)

add_heading_2(doc, "Key Analytical Insights", space_before=2.5, space_after=1)
add_bullet_p(
    doc,
    "Entity Normalization is Critical: ",
    "Abstracting raw numbers, telephone digits, and currency symbols into standardized entity tokens (numtoken, phonetoken, moneytoken) transformed arbitrary character strings into the single most potent class discriminators in the vocabulary.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Handling Class Imbalance: ",
    "The 87.37% to 12.63% class imbalance was effectively mitigated using balanced class weighting during optimization, achieving 0.9542 spam recall without resorting to synthetic oversampling that risks data leakage.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Interpretability via Odds Ratios: ",
    "Converting logistic regression weights into odds ratios reveals that containing a phone number multiplies spam odds by over 512,000x, while URLs multiply odds by 29,465x, providing human-auditable rules for security analysts.",
    font_size=8.8
)

add_heading_2(doc, "Project Limitations", space_before=2.5, space_after=1)
add_bullet_p(
    doc,
    "Simulated Daily Timestamps (Academic Notice): ",
    "A primary limitation of the study is that the UCI SMS Spam Collection benchmark lacks authentic calendar timestamps. Consequently, the daily time-series counts were generated using a simulated temporal baseline with seasonal weekly cycles and Gaussian noise. Real-world telecom telemetry may exhibit burstier diurnal patterns.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Corpus Scale and Morphology: ",
    "The evaluation corpus is constrained to 5,169 English messages primarily originating from UK and Singapore users in the early 2010s, which does not reflect multi-lingual code-mixing, contemporary Unicode homoglyph obfuscation, or emoji-based smishing.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Absence of Real-Time Metadata: ",
    "The current models rely strictly on message body text, without access to network-level signaling attributes such as international dialing prefixes, sender reputation scores, or transmission burst rates.",
    font_size=8.8
)

add_heading_2(doc, "Future Scope", space_before=2.5, space_after=1)
add_bullet_p(
    doc,
    "Transformer-Based Deep Architectures: ",
    "Future work will evaluate lightweight distilled Transformer models (such as DistilBERT and MobileBERT) to capture long-range semantic dependencies and contextual connotations beyond n-gram boundaries.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Multilingual and Multi-Modal Adaptation: ",
    "Expanding the preprocessing architecture to support cross-lingual embeddings, phonetic hashing (Soundex), and optical character recognition for screenshot-based spam.",
    font_size=8.8
)
add_bullet_p(
    doc,
    "Adaptive Streaming and Concept Drift Detection: ",
    "Deploying online incremental learners with drift detectors (such as ADWIN) to continuously adapt vocabulary weights in response to emerging adversarial spam campaigns in live carrier streams.",
    font_size=8.8
)

print(f"Saving filled document to {OUTPUT_DOCX}...")
doc.save(OUTPUT_DOCX)
print("DOCX successfully generated!")

# Convert to PDF via Word COM
print("Converting DOCX to PDF via Word Application COM...")
import subprocess

ps_script = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{OUTPUT_DOCX}')
    $doc.SaveAs([ref]'{OUTPUT_PDF}', [ref]17)
    $doc.Close()
    Write-Host "PDF export successful."
}} catch {{
    Write-Error $_
}} finally {{
    $word.Quit()
}}
"""

res = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
print("PowerShell output:", res.stdout)
if res.stderr:
    print("PowerShell error:", res.stderr)

# Verify page count
try:
    import pymupdf
    pdf_doc = pymupdf.open(OUTPUT_PDF)
    print(f"VERIFIED TOTAL PDF PAGES: {len(pdf_doc)}")
    for i, page in enumerate(pdf_doc):
        first_line = page.get_text().splitlines()[0] if page.get_text().splitlines() else "EMPTY"
        print(f"  Page {i+1}: length {len(page.get_text())} chars | '{first_line[:50]}'")
except Exception as e:
    print("Could not inspect PDF with pymupdf:", e)
