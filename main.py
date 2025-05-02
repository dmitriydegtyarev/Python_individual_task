import requests
from bs4 import BeautifulSoup

url = "https://mvs.gov.ua/"

def main():

    # Надсилання HTTP GET-запиту із обробкою виключень
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на HTTP-помилки
    except requests.exceptions.HTTPError as errh:
        print("HTTP-помилка:", errh)
        return
    except requests.exceptions.ConnectionError as errc:
        print("Помилка з'єднання:", errc)
        return
    except requests.exceptions.Timeout as errt:
        print("Час очікування вичерпано:", errt)
        return
    except requests.exceptions.RequestException as err:
        print("Невідома помилка при запиті:", err)
        return

    # Розбір отриманого HTML-контенту за допомогою BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Завдання 1: Витягнення заголовку сторінки (<title>)
    try:
        title = soup.title.get_text(strip=True) if soup.title else "Без заголовку"
        print("Заголовок сторінки:", title)
    except Exception as e:
        print("Помилка отримання заголовку:", e)

    # Завдання 2: Витягнення метаопису (<meta name="description">) (якщо є)
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        print("Метаопис:", meta_desc.get("content"))
    else:
        print("Метаопис не знайдено.")

    # Завдання 3: Отримання навігаційних посилань
    print("\nНавігаційні посилання:")
    nav_section = soup.find("nav")
    if nav_section:
        nav_links = nav_section.find_all("a")
    else:
        # Якщо тег <nav> не знайдено, виводимо перші 10 посилань зі сторінки
        nav_links = soup.find_all("a")[:10]

    if nav_links:
        for link in nav_links:
            link_text = link.get_text(strip=True)
            link_href = link.get("href", "Немає URL")
            # Виводимо лише посилання з непорожнім текстом
            if link_text:
                print(f"- {link_text}: {link_href}")
    else:
        print("Навігаційні посилання не знайдено.")

    # Завдання 4: Спроба витягнути блок новин/оголошень
    # Припустимо, що інформацію новин можна знайти в елементах, які містять відповідний клас або тег
    print("\nБлок новин/оголошень:")
    # Шукаємо елемент із класом 'news' (це може бути адаптовано під конкретну розмітку)
    news_section = soup.find("div", class_="home-news__content-wrapper")
    if news_section:
        articles = news_section.find_all("li")
        if articles:
            for art in articles:
                # Спроба отримати заголовок новини з тегу <h2> або інший текстовий контент
                header_tag = art.find("h2")
                if header_tag:
                    article_title = header_tag.get_text(strip=True)
                    print(f"- {article_title}")
                else:
                    # Якщо заголовок відсутній, виводимо перший шматок тексту
                    print(f"- {art.get_text(strip=True)[:100]}...")
        else:
            print("У блоці новин знайдено, але не вдалося виділити окремі статті.")
    else:
        print("Блок новин/оголошень не знайдено.")


if __name__ == "__main__":
    main()