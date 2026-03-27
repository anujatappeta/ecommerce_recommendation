# 🛍️ AI-Powered E-Commerce Recommendation System

An intelligent e-commerce web application built using **Reflex (Python)** that provides **personalized product recommendations** using multiple recommendation techniques.

---

## 🚀 Features

* 🔐 User Authentication (Signup/Login)
* 🛒 Add to Cart / Remove from Cart
* ❤️ Wishlist Management
* 📦 View Product Details
* 🔍 Search Products
* 🤖 AI Chatbot for Product Suggestions
* 🎯 Personalized Recommendations:

  * Content-Based Filtering
  * Collaborative Filtering
  * Hybrid Recommendation System
* 💳 Checkout & Payment Simulation
* 📊 Dynamic Product Display

---

## 🧠 Recommendation Techniques Used

* **Content-Based Filtering**
  Recommends products based on user preferences and product features.

* **Collaborative Filtering**
  Suggests items based on similar users’ behavior.

* **Hybrid Model**
  Combines both techniques for better accuracy.

* **Rating-Based System**
  Shows top-rated products for new users.

---

## 🛠️ Tech Stack

* **Frontend & Backend:** Reflex (Python)
* **Database:** CSV-based dataset
* **Machine Learning:** Pandas, Recommendation Algorithms
* **AI Chatbot:** Groq API (LLM)
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
ai_recom/
│── backend/
│   ├── content_based.py
│   ├── collaborative_based.py
│   ├── hybrid.py
│   ├── rating_based.py
│   ├── recommender.py
│   ├── chatbot.py
│
│── components/
│   ├── product_card.py
│   ├── navbar.py
│   ├── footer.py
|   |--chatbot.py
|   |--recommend_product.py
│
│── pages/
│   ├── home.py
│   ├── products.py
│   ├── cart.py
│   ├── checkout.py
|   |--wishlist.py
|   |-- orders.py
│   ├── payment.py
|   |--payment_state.py
│   ├── product_details.py
│   ├── recommendations.py
│   ├── login.py
│   ├── signup.py
|   |--profile.py
|   |--products.py
|   |--config.py
│
│── state.py
│── ai_recom.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/anujatappeta/ecommerce_recommendation.git
cd ecommerce_recommendation
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```
python -m reflex run
```

App will run at:

```
http://localhost:3000
```

---

## 🎥 Demo Video

[![Watch Demo](https://img.icons8.com/color/96/video.png)](https://drive.google.com/file/d/1aEN8uKSxQhRzK9iUCS8SqIPO6qzBSs7H/preview)
---

## 💡 Future Improvements

* 🧠 Advanced Deep Learning Recommendations
* 💳 Real Payment Integration (Razorpay/Stripe)
* 🌐 Deployment (Render/Vercel/Azure)
* 📱 Mobile Responsive UI
* 🗄️ Database Integration (PostgreSQL/MongoDB)

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork and improve the project.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👩‍💻 Author

**Anuja Tappeta**
