"""Chapter 07 Streamlit 앱: 도서 분야 예측 + 비슷한 도서 추천.

Chapter 07 노트북(chapter07.ipynb)에서 검증한 개선 파이프라인
(Kiwi 형태소 분석 -> 명사/영문 필터링 -> TF-IDF -> Naive Bayes / Cosine Similarity)을
그대로 앱에 연결합니다. 배포용 모델은 평가용 train/test 분할이 아니라
전체 books_improved.csv로 학습합니다(평가는 chapter07.ipynb에서 이미 완료).
"""

import streamlit as st
import pandas as pd
from kiwipiepy import Kiwi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "books/books_improved.csv"
KEEP_TAGS = {"NNG", "NNP", "SL"}
STOPWORDS = {"에디션"}


@st.cache_resource
def load_kiwi():
    return Kiwi()


def is_meaningful(token: str) -> bool:
    if len(token) < 2:
        return False
    if token.isdigit():
        return False
    if token in STOPWORDS:
        return False
    return True


def clean_title(title: str, kiwi: Kiwi) -> str:
    """제목 문자열 -> 형태소 분석 -> 명사/영문 태그만 선택 -> 길이/숫자/불용어 필터."""
    text = str(title) if pd.notna(title) else ""
    tokens = [t.form for t in kiwi.tokenize(text) if t.tag in KEEP_TAGS]
    tokens = [t for t in tokens if is_meaningful(t)]
    return " ".join(tokens)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    kiwi = load_kiwi()
    df["상품명_정제"] = df["상품명"].apply(lambda title: clean_title(title, kiwi))
    return df


@st.cache_resource
def train_classifier(df: pd.DataFrame):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["상품명_정제"])
    model = MultinomialNB()
    model.fit(X, df["분야"])
    return vectorizer, model


@st.cache_resource
def build_recommendation_matrix(df: pd.DataFrame):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(df["상품명_정제"])
    similarity = cosine_similarity(matrix)
    return similarity


def predict_category(title: str, kiwi: Kiwi, vectorizer, model):
    refined = clean_title(title, kiwi)
    vec = vectorizer.transform([refined])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    top3_idx = proba.argsort()[::-1][:3]
    top3 = [(model.classes_[i], proba[i]) for i in top3_idx]
    return pred, top3, refined


def recommend_books(index: int, df: pd.DataFrame, similarity, top_n: int = 5):
    """같은 분야 + 자기 자신 제외 + 유사도 0 초과 조건으로 Top N을 뽑는다.

    조건을 만족하는 후보가 top_n보다 적으면 있는 만큼만 반환한다(억지로 채우지 않음).
    """
    category = df.loc[index, "분야"]
    candidate_idx = df.index[df["분야"] == category]

    scored = [
        (i, similarity[index, i])
        for i in candidate_idx
        if i != index and similarity[index, i] > 0
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:top_n]
    return [(df.loc[i, "상품명"], score) for i, score in top]


st.set_page_config(page_title="도서 분야 예측 & 추천 (Chapter 07)", layout="centered")
st.title("도서 분야 예측 & 비슷한 도서 추천")
st.caption("Chapter 07 개선 파이프라인: Kiwi 형태소 분석 + 명사/영문 필터 + TF-IDF + Naive Bayes / Cosine Similarity")

kiwi = load_kiwi()
df = load_data()
vectorizer, model = train_classifier(df)
similarity_matrix = build_recommendation_matrix(df)

menu = st.radio("메뉴를 선택하세요", ["1. 도서 분야 예측", "2. 비슷한 도서 추천"])

if menu == "1. 도서 분야 예측":
    st.subheader("도서 제목으로 분야 예측하기")
    title_input = st.text_input("도서 제목을 입력하세요", value="처음 배우는 파이썬 데이터 분석")

    if title_input.strip():
        pred, top3, refined = predict_category(title_input, kiwi, vectorizer, model)
        st.write(f"**정제된 텍스트**: `{refined}`")
        st.success(f"예상 분야: **{pred}**")
        st.write("상위 3개 확률")
        for category, prob in top3:
            st.write(f"- {category}: {prob:.2%}")
    else:
        st.info("제목을 입력하면 예상 분야가 표시됩니다.")

else:
    st.subheader("비슷한 도서 추천")
    title_options = df["상품명"].tolist()
    selected_title = st.selectbox("기준이 될 도서를 선택하세요", title_options)
    selected_index = df.index[df["상품명"] == selected_title][0]

    st.write(f"선택한 도서 분야: **{df.loc[selected_index, '분야']}**")

    results = recommend_books(selected_index, df, similarity_matrix, top_n=5)

    if results:
        st.write("추천 도서 (같은 분야, 유사도 0 초과, 유사도 높은 순)")
        for rank, (title, score) in enumerate(results, start=1):
            st.write(f"{rank}. {title} (유사도 {score:.3f})")
    else:
        st.warning("현재 기준으로 유사도가 있는 추천 도서를 찾지 못했습니다.")
