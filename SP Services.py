from flask import Flask, render_template_string, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

REVIEWS_FILE = Path("reviews.json")

def load_reviews():
    if not REVIEWS_FILE.exists():
        return {}
    try:
        return json.loads(REVIEWS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

def save_reviews(reviews):
    REVIEWS_FILE.write_text(
        json.dumps(reviews, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SP SERVICES</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: Inter, Arial, sans-serif;
    background: #050507;
    color: #f5f5f7;
    min-height: 100vh;

    background-image:
        linear-gradient(rgba(139,70,255,.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(139,70,255,.055) 1px, transparent 1px);

    background-size: 38px 38px;
}

body:before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(132,44,255,.12),
            transparent 38%
        );
}

header {
    height: 76px;
    position: sticky;
    top: 0;
    z-index: 20;

    display: flex;
    align-items: center;

    border-bottom: 1px solid #17171d;

    background: rgba(4,4,6,.88);
    backdrop-filter: blur(14px);
}

.nav {
    width: min(1120px,92%);
    margin: auto;

    display: flex;
    align-items: center;
    gap: 38px;
}

.logo {
    font-weight: 800;
    letter-spacing: 3px;
    font-size: 20px;
    margin-right: auto;
}

nav {
    display: flex;
    gap: 30px;
    align-items: center;
}

nav a {
    color: #d2d2d8;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
}

nav a:hover {
    color: #a85cff;
}

.nav-btn {
    border: 1px solid #6730a8;
    background: #100a1a;
    padding: 10px 15px;
    border-radius: 5px;
}

.discord {
    background: #5865f2;
    color: white !important;
    padding: 11px 20px;
    border-radius: 5px;
}

.support {
    background: #7d2ff0;
    color: white !important;
    padding: 11px 20px;
    border-radius: 5px;
}

.support:hover {
    filter: brightness(1.12);
}

.hero {
    width: min(1120px,92%);
    margin: 0 auto;
    padding: 100px 0 55px;
    text-align: center;
}

.badge {
    display: inline-block;

    border: 1px solid #3b2357;
    background: #0d0813;
    color: #a85cff;

    padding: 7px 12px;
    border-radius: 5px;

    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;

    margin-bottom: 22px;
}

h1 {
    font-size: clamp(42px,7vw,72px);
    line-height: 1.02;
    letter-spacing: -3px;
}

.gradient {
    background: linear-gradient(90deg,#8c36ff,#c25cff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero p {
    max-width: 650px;
    margin: 22px auto 30px;

    color: #92929c;

    font-size: 16px;
    line-height: 1.7;
}

.cta {
    display: inline-flex;
    gap: 12px;
    align-items: center;

    padding: 14px 24px;
    border-radius: 6px;

    color: white;
    text-decoration: none;

    font-weight: 700;
    font-size: 14px;

    background: linear-gradient(90deg,#7d2ff0,#ad4cff);

    box-shadow: 0 0 30px rgba(145,57,255,.18);
}

.section {
    width: min(1120px,92%);
    margin: 0 auto;
    padding: 30px 0 90px;
}

.section-title {
    margin-bottom: 28px;
}

.section-title h2 {
    font-size: 28px;
}

.section-title p {
    color: #777782;
    margin-top: 7px;
    font-size: 14px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 26px;
}

.card {
    background: linear-gradient(180deg,#101013,#0c0c0f);

    border: 1px solid #25252c;
    border-radius: 12px;

    padding: 30px 28px 27px;

    transition:
        .2s transform,
        .2s border-color,
        .2s box-shadow;
}

.card:hover {
    transform: translateY(-4px);

    border-color: #7d3be0;

    box-shadow:
        0 10px 35px rgba(126,45,255,.11);
}

.tag {
    display: inline-block;

    border: 1px solid #303038;
    color: #8d8d99;

    padding: 4px 7px;
    border-radius: 4px;

    font-size: 9px;
    letter-spacing: .8px;

    margin-bottom: 19px;
}

.card h3 {
    font-size: 21px;
    margin-bottom: 11px;
}

.price {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 22px;
}

.features {
    list-style: none;
    min-height: 66px;
}

.features li {
    color: #a9a9b2;
    font-size: 13px;
    margin: 11px 0;
}

.features li:before {
    content: "✓";
    color: #9b48ff;
    margin-right: 9px;
}

.buy {
    width: 100%;

    border: 0;
    border-radius: 7px;

    padding: 13px;

    color: #fff;

    font-weight: 800;
    font-size: 13px;
    letter-spacing: .3px;

    background: linear-gradient(90deg,#7c2fed,#aa4bed);

    cursor: pointer;
    margin-top: 12px;
}

.buy:hover {
    filter: brightness(1.12);
}

.view-product {
    width: 100%;
    border: 1px solid #6730a8;
    border-radius: 7px;
    padding: 11px;
    color: #c99cff;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: .3px;
    background: #100a1a;
    cursor: pointer;
    margin-top: 9px;
}

.view-product:hover {
    background: #1a0e2a;
    border-color: #9b48ff;
}

.stock {
    display: inline-block;
    margin-top: 5px;
    padding: 5px 8px;
    border-radius: 5px;
    background: #17101f;
    color: #b978ff;
    font-size: 11px;
    font-weight: 700;
}

.product-modal-box {
    width: min(520px,100%);
    background: #101014;
    border: 1px solid #332047;
    border-radius: 12px;
    padding: 28px;
    box-shadow: 0 20px 80px #000;
}

.product-info {
    display: grid;
    gap: 12px;
    margin-top: 20px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 13px 14px;
    background: #08080b;
    border: 1px solid #25252c;
    border-radius: 7px;
}

.info-label {
    color: #777782;
    font-size: 13px;
}

.info-value {
    color: #f5f5f7;
    font-size: 13px;
    font-weight: 700;
    text-align: right;
}

.reviews {
    color: #ffc857;
    letter-spacing: 1px;
}

.next-discount {
    color: #a85cff;
}

.rating-area {
    margin-top: 22px;
    padding-top: 20px;
    border-top: 1px solid #25252c;
}

.rating-area h3 {
    font-size: 16px;
    margin-bottom: 10px;
}

.stars {
    display: flex;
    gap: 6px;
    margin-bottom: 14px;
}

.star {
    border: 1px solid #332047;
    background: #08080b;
    color: #555562;
    width: 42px;
    height: 42px;
    border-radius: 7px;
    font-size: 22px;
    cursor: pointer;
    transition: .15s;
}

.star:hover,
.star.selected {
    color: #ffc857;
    border-color: #9b48ff;
    background: #17101f;
}

.review-input {
    width: 100%;
    min-height: 95px;
    resize: vertical;
    background: #08080b;
    border: 1px solid #292932;
    color: white;
    padding: 13px;
    border-radius: 7px;
    outline: none;
    font-family: Inter, Arial, sans-serif;
    font-size: 13px;
}

.review-input:focus {
    border-color: #7d3be0;
}

.review-message {
    min-height: 18px;
    margin-top: 9px;
    color: #8f8f99;
    font-size: 12px;
}

.saved-reviews {
    margin-top: 18px;
    display: grid;
    gap: 10px;
}

.saved-review {
    background: #08080b;
    border: 1px solid #25252c;
    border-radius: 7px;
    padding: 12px;
}

.saved-review .review-stars {
    color: #ffc857;
    margin-bottom: 5px;
}

.saved-review p {
    color: #b1b1ba;
    font-size: 12px;
    line-height: 1.6;
}

footer {
    border-top: 1px solid #19191f;

    padding: 30px 0;

    text-align: center;

    color: #666672;
    font-size: 12px;
}

.modal {
    display: none;

    position: fixed;
    inset: 0;
    z-index: 50;

    background: rgba(0,0,0,.75);

    align-items: center;
    justify-content: center;

    padding: 20px;
}

.modal.open {
    display: flex;
}

.modal-box {
    width: min(450px,100%);

    background: #101014;

    border: 1px solid #332047;
    border-radius: 12px;

    padding: 28px;

    box-shadow: 0 20px 80px #000;
}

.modal-box h2 {
    margin-bottom: 8px;
}

.modal-box p {
    color: #8d8d97;
    font-size: 13px;
    line-height: 1.6;
}

.close {
    float: right;

    background: none;
    border: 0;

    color: #777;
    font-size: 24px;

    cursor: pointer;
}

.form {
    display: flex;
    flex-direction: column;
    gap: 10px;

    margin-top: 20px;
}

.form input {
    background: #08080b;

    border: 1px solid #292932;

    color: white;

    padding: 13px;

    border-radius: 6px;

    outline: none;
}

@media(max-width:850px) {

    .grid {
        grid-template-columns: 1fr 1fr;
    }

    nav {
        gap: 13px;
    }

    nav a:nth-child(2),
    nav a:nth-child(3) {
        display: none;
    }
}

@media(max-width:600px) {

    .grid {
        grid-template-columns: 1fr;
    }

    .nav {
        gap: 12px;
    }

    .logo {
        font-size: 15px;
    }

    .discord,
    .support {
        padding: 9px 12px;
    }
}
</style>
</head>

<body>

<header>

<div class="nav">

<div class="logo">
SP SERVICES
</div>

<nav>

<a href="#home">Home</a>

<a href="#services">Services</a>

<a href="#about">About</a>

<a class="nav-btn" href="#services">
SHOP
</a>

<a class="nav-btn" href="#track">
⌕ Track Order
</a>

<a
class="discord"
href="https://discord.gg/MUz3QVF9d"
target="_blank"
rel="noopener noreferrer">
▢ Discord
</a>

<a
class="support"
href="https://discord.gg/XvYsCe6qx"
target="_blank"
rel="noopener noreferrer">
🛠 Support
</a>

</nav>

</div>

</header>


<section class="hero" id="home">

<span class="badge">
TRUSTED DIGITAL SERVICES
</span>

<h1>
MARLEY
<span class="gradient">
SERVICES
</span>
</h1>

<p>
Premium digital services, custom solutions and products.
Browse our services below and choose what works for you.
</p>

<a class="cta" href="#services">
VIEW SERVICES →
</a>

</section>


<section class="section" id="services">

<div class="section-title">

<h2>
Featured Services
</h2>

<p>
Choose a service and get started.
</p>

</div>


<div class="grid">


<div class="card">

<span class="tag">
DIGITAL
</span>

<h3>
Discord Setup
</h3>

<div class="price">
£5.00
</div>

<ul class="features">

<li>
Custom server setup
</li>

<li>
Roles & permissions
</li>

<li>
Channel organisation
</li>

</ul>

<button
class="buy"
onclick="openBuy('Discord Setup')">
PURCHASE
</button>

<button
class="view-product"
onclick="viewProduct('Discord Setup', '8', '4.9/5', '12 reviews', '10% off when 3+ are ordered')">
VIEW
</button>

</div>


<div class="card">

<span class="tag">
POPULAR
</span>

<h3>
Custom Discord Bot
</h3>

<div class="price">
£10.00
</div>

<ul class="features">

<li>
Custom commands
</li>

<li>
Moderation features
</li>

<li>
Setup assistance
</li>

</ul>

<button
class="buy"
onclick="openBuy('Custom Discord Bot')">
PURCHASE
</button>

<button
class="view-product"
onclick="viewProduct('Custom Discord Bot', '5', '5.0/5', '8 reviews', '15% off next Friday')">
VIEW
</button>

</div>


<div class="card">

<span class="tag">
DESIGN
</span>

<h3>
Profile Graphics
</h3>

<div class="price">
£1.00
</div>

<ul class="features">

<li>
Custom profile picture
</li>

<li>
High quality design
</li>

<li>
Revisions included
</li>

</ul>

<button
class="buy"
onclick="openBuy('Profile Graphics')">
PURCHASE
</button>

<button
class="view-product"
onclick="viewProduct('Profile Graphics', '14', '4.8/5', '21 reviews', '20% off after 5 orders')">
VIEW
</button>

</div>


<div class="card">

<span class="tag">
WEB
</span>

<h3>
Website Design
</h3>

<div class="price">
£20.00
</div>

<ul class="features">

<li>
Modern responsive design
</li>

<li>
Custom branding
</li>

<li>
Mobile friendly
</li>

</ul>

<button
class="buy"
onclick="openBuy('Website Design')">
PURCHASE
</button>

<button
class="view-product"
onclick="viewProduct('Website Design', '3', '5.0/5', '6 reviews', '10% off next week')">
VIEW
</button>

</div>


<div class="card">

<span class="tag">
DEVELOPMENT
</span>

<h3>
Roblox Development
</h3>

<div class="price">
£5.00
</div>

<ul class="features">

<li>
Game systems
</li>

<li>
UI and scripting
</li>

<li>
Custom requests
</li>

</ul>

<button
class="buy"
onclick="openBuy('Roblox Development')">
PURCHASE
</button>

<button
class="view-product"
onclick="viewProduct('Roblox Development', '7', '4.7/5', '11 reviews', '15% off this weekend')">
VIEW
</button>

</div>


<div class="card">

<span class="tag">
PREMIUM
</span>

<h3>
Full Custom Package
</h3>

<div class="price">
£40.00
</div>

<ul class="features">

<li>
Discord + website
</li>

<li>
Custom graphics
</li>

<li>
Priority support
</li>

</ul>

<button
class="buy"
onclick="openBuy('Full Custom Package')">
PURCHASE
</button>

<button
class="view-product"
onclick="viewProduct('Full Custom Package', '2', '5.0/5', '5 reviews', '£5 off the next package')">
VIEW
</button>

</div>


</div>

</section>


<section class="section" id="about">

<div class="section-title">

<h2>
About SP SERVICES
</h2>

<p>
Simple, modern and affordable digital services.
</p>

</div>


<div class="card">

<p style="color:#999;line-height:1.8;font-size:14px">

Welcome to SP SERVICES! I am a small
Online entrepreneur looking to become succsesful
through selling services online


</p>

</div>

</section>


<section class="section" id="track">

<div class="section-title">

<h2>
Track Order
</h2>

<p>
Enter your order number to check its status.
</p>

</div>


<div class="card" style="max-width:600px">

<div class="form">

<input
id="orderInput"
placeholder="Order number"
>

<button
class="buy"
onclick="trackOrder()">

TRACK ORDER

</button>

<p
id="trackResult"
style="color:#8f8f99;font-size:13px">
</p>

</div>

</div>

</section>


<footer>

© 2026 SP SERVICES. All rights reserved.

</footer>


<div class="modal" id="productModal">

<div class="product-modal-box">

<button
class="close"
onclick="closeProduct()">
×
</button>

<h2 id="productTitle">
Product Details
</h2>

<p>
See current stock, customer reviews and the next discount for this product.
</p>

<div class="product-info">

<div class="info-row">
<span class="info-label">Stock left</span>
<span class="info-value" id="productStock"></span>
</div>

<div class="info-row">
<span class="info-label">Reviews</span>
<span class="info-value reviews" id="productRating"></span>
</div>

<div class="info-row">
<span class="info-label">Review count</span>
<span class="info-value" id="productReviews"></span>
</div>

<div class="info-row">
<span class="info-label">Next discount</span>
<span class="info-value next-discount" id="productDiscount"></span>
</div>

</div>

<div class="rating-area">

<h3>Leave a review</h3>

<div class="stars" id="ratingStars">
    <button class="star" onclick="selectRating(1)">★</button>
    <button class="star" onclick="selectRating(2)">★</button>
    <button class="star" onclick="selectRating(3)">★</button>
    <button class="star" onclick="selectRating(4)">★</button>
    <button class="star" onclick="selectRating(5)">★</button>
</div>

<textarea
    id="reviewInput"
    class="review-input"
    placeholder="Write your review..."></textarea>

<button
class="buy"
onclick="submitReview()">
SUBMIT REVIEW
</button>

<p id="reviewMessage" class="review-message"></p>

<div id="savedReviews" class="saved-reviews"></div>

</div>

<button
class="buy"
onclick="closeProduct()">
CLOSE
</button>

</div>

</div>


<div class="modal" id="modal">

<div class="modal-box">

<button
class="close"
onclick="closeBuy()">

×

</button>

<h2 id="modalTitle">
Purchase
</h2>

<p>

To purchase this service,
replace this section with your
payment link, checkout system
or Discord ticket link.

</p>

<div class="form">

<input
placeholder="Your Discord username"
>

<button
class="buy"
onclick="alert('Connect your payment system here.')">

CONTINUE

</button>

</div>

</div>

</div>


<script>

let currentProduct = "";
let selectedRating = 0;

function viewProduct(name, stock, rating, reviews, discount) {
    currentProduct = name;

    document.getElementById("productTitle").textContent = name;
    document.getElementById("productStock").textContent = stock + " available";
    document.getElementById("productRating").textContent = "★ " + rating;
    document.getElementById("productReviews").textContent = reviews;
    document.getElementById("productDiscount").textContent = discount;

    selectedRating = 0;
    updateStars();
    document.getElementById("reviewInput").value = "";
    document.getElementById("reviewMessage").textContent = "";

    loadReviews();

    document.getElementById("productModal").classList.add("open");
}

function selectRating(rating) {
    selectedRating = rating;
    updateStars();
}

function updateStars() {
    document.querySelectorAll("#ratingStars .star").forEach((star, index) => {
        star.classList.toggle("selected", index < selectedRating);
    });
}

async function submitReview() {
    const reviewText = document.getElementById("reviewInput").value.trim();
    const message = document.getElementById("reviewMessage");

    if (selectedRating === 0) {
        message.textContent = "Please choose a star rating first.";
        return;
    }

    if (!reviewText) {
        message.textContent = "Please write a review first.";
        return;
    }

    try {
        const response = await fetch("/api/reviews", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                product: currentProduct,
                rating: selectedRating,
                text: reviewText
            })
        });

        const result = await response.json();

        if (!response.ok) {
            message.textContent = result.error || "Could not save your review.";
            return;
        }

        document.getElementById("reviewInput").value = "";
        selectedRating = 0;
        updateStars();
        message.textContent = "Thanks! Your review has been saved.";
        loadReviews();

    } catch (error) {
        message.textContent = "Could not connect to the review server.";
    }
}

async function loadReviews() {
    const container = document.getElementById("savedReviews");
    container.innerHTML = "";

    try {
        const response = await fetch(
            "/api/reviews?product=" + encodeURIComponent(currentProduct)
        );
        const reviews = await response.json();

        reviews.slice().reverse().forEach(review => {
            const item = document.createElement("div");
            item.className = "saved-review";

            const stars = document.createElement("div");
            stars.className = "review-stars";
            stars.textContent =
                "★".repeat(review.rating) +
                "☆".repeat(5 - review.rating);

            const paragraph = document.createElement("p");
            paragraph.textContent = review.text;

            item.appendChild(stars);
            item.appendChild(paragraph);
            container.appendChild(item);
        });

    } catch (error) {
        container.innerHTML =
            '<p style="color:#777782;font-size:12px;">Unable to load reviews.</p>';
    }
}

function closeProduct() {
    document.getElementById("productModal").classList.remove("open");
}

function openBuy(name) {

    document.getElementById("modalTitle").textContent =
        "Purchase — " + name;

    document.getElementById("modal").classList.add("open");
}


function closeBuy() {

    document.getElementById("modal").classList.remove("open");
}


function trackOrder() {

    const value =
        document.getElementById("orderInput").value.trim();

    document.getElementById("trackResult").textContent =
        value
        ? "Order " + value +
          " is being checked. Connect this to your order database to show live status."
        : "Please enter an order number.";
}


document.getElementById("productModal").addEventListener(
    "click",
    function(event) {
        if (event.target.id === "productModal") {
            closeProduct();
        }
    }
);

document.getElementById("modal").addEventListener(
    "click",
    function(event) {

        if (event.target.id === "modal") {

            closeBuy();

        }

    }
);

</script>

</body>
</html>
"""


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    product = request.args.get("product", "").strip()
    reviews = load_reviews()
    return jsonify(reviews.get(product, []))


@app.route("/api/reviews", methods=["POST"])
def add_review():
    data = request.get_json(silent=True) or {}
    product = str(data.get("product", "")).strip()
    review_text = str(data.get("text", "")).strip()

    try:
        rating = int(data.get("rating"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid rating."}), 400

    if not product:
        return jsonify({"error": "Product is required."}), 400
    if rating < 1 or rating > 5:
        return jsonify({"error": "Rating must be between 1 and 5."}), 400
    if not review_text:
        return jsonify({"error": "Review cannot be empty."}), 400
    if len(review_text) > 1000:
        return jsonify({"error": "Review is too long."}), 400

    reviews = load_reviews()
    reviews.setdefault(product, []).append({
        "rating": rating,
        "text": review_text
    })
    save_reviews(reviews)

    return jsonify({"success": True})


@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
