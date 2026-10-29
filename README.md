# PC mart — Computer Components E-Commerce Catalog

A clean, responsive full-stack e-commerce catalog for computer hardware and peripherals built with **Python (Flask)**, **SQLite**, **HTML5**, **CSS3**, **JavaScript**, and **Bootstrap 5**.

---

## Tech Stack

### Front-End
- **HTML5**: Semantic web markup (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`).
- **CSS3**: Custom downward fading light-blue-to-white background gradient, card hover elevations, smooth transitions, and carousel layout (`static/css/style.css`).
- **JavaScript (ES6+)**: Live debounced search, dynamic category filtering, clickable cards directly linking to product pages, and dynamic 5-item featured carousel (`static/js/main.js`).
- **Bootstrap 5**: Grid system, navbar, badges, carousel component, and Bootstrap Icons.

### Back-End
- **Python (Flask)**: Lightweight server serving frontend templates and REST API endpoints.
- **SQLite3**: Relational database storing 30 components across 10 categories with prices in Indian Rupees (₹).

---

## Categories (30 items total, 3 per category)

1. **Cabinet**
2. **Motherboard**
3. **CPU**
4. **GPU**
5. **RAM**
6. **Keyboard**
7. **Mouse**
8. **Speakers**
9. **Headphones**
10. **Game Controllers**

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/products` | Retrieve all products (supports `?search=` and `?category=`) |
| `GET` | `/api/products/<id>` | Retrieve details of a specific product by ID |
| `GET` | `/api/products/featured` | Retrieve 5 random products for the featured carousel (supports `?exclude=<id>`) |
| `GET` | `/api/categories` | Retrieve the 10 component categories in order |
| `GET` | `/` | Main PC mart catalog webpage |
| `GET` | `/product/<id>` | Product details page with featured products carousel |

---

## Deployment Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**:
   ```bash
   python init_db.py
   ```
   *(Note: `app.py` also checks and auto-seeds the 30 products on first run if needed).*

3. **Start the Flask Server**:
   ```bash
   python app.py
   ```

4. **Visit in Browser**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000)
