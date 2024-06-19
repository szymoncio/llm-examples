import openai
import streamlit as st

# Funkcja inicjalizująca API klienta OpenAI
def get_openai_client(api_key):
    openai.api_key = api_key

# Pobranie klucza API z sekcji secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Inicjalizacja klienta OpenAI
get_openai_client(openai_api_key)

# Tytuł aplikacji
st.title("🗜️ Generowanie podsumowania")
st.write("Wprowadź tekst i skróć do do trzech punktów. Wykorzystuje API GPT i model GPT-4o.")


# Using "with" notation
with st.sidebar:
    count = st.number_input("Liczba punktów", min_value=1, max_value=10, value=3, step=1)
    GPTmodel = st.selectbox("Model", ["gpt-4o", "gpt-3.5-turbo"], index=0)
    temperatura = st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.5, step=0.1)



# Sekcja z instrukcjami
with st.expander("Zobacz prompt"):
    # Pole tekstowe do wprowadzania reguł (predefiniowany prompt)
    rules = st.text_area("Treść prompta (mozna edytować)", value="Podsumuj tekst", height=None, key="rules", placeholder="Podaj prompt")


# Pole tekstowe do wprowadzania tekstu, który ma być zmodyfikowany
text_to_modify = st.text_area("Podaj tekst", value="", height=None, key="text_to_modify")

if st.button("Wygeneruj skrót"):

    # Tworzenie promptu na podstawie reguł i tekstu
    prompt = f"Zmień tekst: '{text_to_modify}' według następujących reguł: {rules} oraz skróć do {count} punktów."

    # Inicjalizacja listy wiadomości w sesji
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.session_state.messages.append({"role": "user", "content": prompt})
 #   st.chat_message("user").write(prompt)

    # Wysłanie zapytania do API OpenAI

    # Inicjalizacja listy wiadomości
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model=GPTmodel, messages=messages, temperature=temperatura)
    st.session_state["response"] = response.choices[0].message.content
    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
    st.write(st.session_state["response"])

