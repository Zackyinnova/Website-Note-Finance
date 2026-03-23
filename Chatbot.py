import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# DATA FAQ
# =========================
qa_data = [
    {"question": "Bagaimana Cara Menambah Pendapatan",
     "answer": "Anda bisa memulai investasi seperti saham, emas, dan crypto"},

    {"question": "Berikan strategi menabung",
     "answer": "Gunakan metode 50% kebutuhan, 30% hiburan, 20% tabungan"},

    {"question": "Berikan strategi berinvestasi",
     "answer": "Alokasikan 40% reksa dana, 30% saham, 20% emas, 10% crypto"}
]

df = pd.DataFrame(qa_data)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["question"])

# =========================
# FLOW
# =========================
flows = {
    "investasi": {
        "pendek": {
            "next": "investasi_pendek",
            "response": "Untuk jangka pendek, kamu bisa pilih deposito atau reksa dana pasar uang."
        },
        "menengah": {
            "next": "investasi_menengah",
            "response": "Untuk jangka menengah, kamu bisa pilih obligasi, emas, atau saham bluechip."
        },
        "panjang": {
            "next": "investasi_panjang",
            "response": "Untuk jangka panjang, kamu bisa pilih saham besar, reksa dana saham, atau crypto."
        }
    },

    "investasi_pendek": {
        "deposito": {
            "response": "Kami menyarankan bank seperti BCA, Mandiri, BNI, atau BRI."
        },
        "reksa dana": {
            "response": "Reksa dana pasar uang cocok untuk risiko rendah."
        }
    },

    "investasi_menengah": {
        "obligasi": {
            "response": "Kami menyarankan ORI dan sukuk ritel."
        },
        "emas": {
            "response": "Anda bisa beli emas fisik atau digital seperti di Pluang."
        },
        "saham": {
            "response": "Saham bluechip seperti BBCA, BBRI, BMRI cocok."
        }
    },

    "investasi_panjang": {
        "saham": {
            "response": "Fokus saham growth dan investasi rutin."
        },
        "crypto": {
            "response": "Bitcoin dan Ethereum adalah pilihan populer."
        }
    }
}

# =========================
# STATE
# =========================
context = None

# =========================
# CHATBOT FUNCTION (UNTUK FLASK)
# =========================
def get_chatbot_response(user_input, threshold=0.3):
    global context
    user_input = user_input.lower()

    # FLOW
    if context:
        current_flow = flows.get(context, {})

        for key in current_flow:
            if key in user_input:
                node = current_flow[key]

                if "next" in node:
                    context = node["next"]
                else:
                    context = None

                return node["response"]

    # TF-IDF
    user_vector = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vector, tfidf_matrix)

    best_index = similarity.argmax()
    best_score = similarity.max()

    # trigger flow
    if "investasi" in user_input:
        context = "investasi"
        return "Kamu mau jangka pendek, menengah, atau panjang?"

    if best_score < threshold:
        return "Maaf, saya belum mengerti."

    return df.iloc[best_index]["answer"]