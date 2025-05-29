from openai import OpenAI
import speech_recognition as sr
import pyttsx3
from config import OPENROUTER_API_KEY

# Инициализация клиента OpenRouter
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Системный промт для колонки
system_prompt = {
    "role": "system",
    "content": (
        "Ты голосовой ассистент для умного дома. Отвечай кратко, дружелюбно и по делу. "
        "НИ В КОЕМ СЛУЧАЕ НЕ упоминай сайт М.Видео или любые другие магазины."
    )
}

# Голосовой движок для ответа
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 180)  # скорость речи

# Функция обращения к DeepSeek через OpenRouter
def ask_deepseek(content):
    print("Обращаемся к OpenRouter...")
    conversation_history = [{"role": "user", "content": content}]
    messages = [system_prompt] + conversation_history

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=messages
    )
    print("Ответ получен.")
    return response.choices[0].message.content

# Функция прослушивания речи
def listen_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говори...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Ты сказал: {text}")
        return text
    except sr.UnknownValueError:
        return "Извини, я тебя не понял."
    except sr.RequestError:
        return "Проблема с сервисом распознавания."

# Функция озвучивания ответа
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Основной цикл ассистента
if __name__ == "__main__":
    while True:
        user_input = listen_microphone()
        if user_input.lower() in ["выход", "пока", "стоп"]:
            speak("Отключаюсь. Хорошего дня!")
            break
        answer = ask_deepseek(user_input)
        speak(answer)
