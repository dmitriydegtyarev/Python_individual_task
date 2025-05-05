import requests
from bs4 import BeautifulSoup
import json

JSON_FILE = "mvs_data.json"
URL = "https://mvs.gov.ua/"

# Функція для отримання HTML-розмітки
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as err:
        print(f"Помилка запиту: {err}")
        return None

# Функція для збереження даних у JSON-файл
def save_to_json(data, category):
    try:
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            json_data = {}

        json_data[category] = data

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        print(f"Дані збережено у {JSON_FILE} в категорію '{category}'")
    except Exception as e:
        print(f"Помилка при записі JSON: {e}")

# Взаємодія з користувачем
def main():
    html = get_html(URL)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")

    while True:
        print("\nОберіть дію:"
              "\n1 - Зчитати заголовок сторінки"
              "\n2 - Отримати метаопис"
              "\n3 - Витягнути навігаційні посилання"
              "\n4 - Витягнути заголовки новин"
              "\n5 - Вихід\n")

        choice = input("Введіть номер операції: ")

        if choice == "1":
            title = soup.title.get_text(strip=True) if soup.title else "Без заголовку"
            print("\nЗаголовок сторінки:", title)
            save_to_json({"title": title}, "Заголовок")

        elif choice == "2":
            meta_desc = soup.find("meta", attrs={"name": "description"})
            meta_text = meta_desc["content"] if meta_desc and meta_desc.get("content") else "Метаопис не знайдено"
            print("\nМетаопис:", meta_text)
            save_to_json({"meta_description": meta_text}, "Метаопис")

        elif choice == "3":
            nav_section = soup.find("nav")
            nav_links = nav_section.find_all("a") if nav_section else soup.find_all("a")[:10]
            links_data = [{"text": link.get_text(strip=True), "url": link.get("href", "Немає URL")} for link in nav_links if link.get_text(strip=True)]

            print("\nНавігаційні посилання:")
            for link in links_data:
                print(f"- {link['text']}: {link['url']}")

            save_to_json(links_data, "Навігація")

        elif choice == "4":
            news_section = soup.find("div", class_="home-news__content-wrapper")
            articles = news_section.find_all("li") if news_section else []
            news_data = [{"title": art.find("h2").get_text(strip=True) if art.find("h2") else art.get_text(strip=True)[:100]} for art in articles]

            if news_data:
                print("\nЗаголовки новин:")
                for news in news_data:
                    print(f"- {news['title']}")
            else:
                print("\nБлок новин не знайдено.")

            save_to_json(news_data, "Новини")

        elif choice == "5":
            print("\nЗавершення роботи.")
            break
        else:
            print("\nНевірний вибір. Спробуйте знову.")

# Залишаємо можливість для рефакторінгу коду і розділення на окремі модулі в майбутньому
if __name__ == "__main__":
    main()