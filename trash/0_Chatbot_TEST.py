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
st.title("💬 Chatbot_TEST")

# Sekcja z instrukcjami
with st.expander("See explanation"):
    st.write("Wprowadź reguły w polu poniżej oraz tekst, który chcesz zmienić zgodnie z tymi regułami.")

# Pole tekstowe do wprowadzania reguł (predefiniowany prompt)
rules = st.text_area("Reguły", value="Podaj tutaj swoje reguły", height=None, key="rules")

# Pole tekstowe do wprowadzania tekstu, który ma być zmodyfikowany
text_to_modify = st.text_area("Tekst do zmiany", value="", height=None, key="text_to_modify")

if st.button("Wyślij zapytanie"):

    # Tworzenie promptu na podstawie reguł i tekstu
    prompt = f"Zmień tekst: '{text_to_modify}' według następujących reguł: {rules}"

    # Inicjalizacja listy wiadomości w sesji
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Wysłanie zapytania do API OpenAI

    # Inicjalizacja listy wiadomości
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    st.session_state["response"] = response.choices[0].message.content
    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
    st.write(st.session_state["response"])