const products = document.querySelectorAll(".product");
const totalCount = document.getElementById("total-count");
const totalPrice = document.getElementById("total-price");

function updateCart() {
    let count = 0;
    let price = 0;

    products.forEach(product => {
        const productPrice = Number(product.dataset.price);
        const quantity = Number(product.querySelector(".count").textContent);

        count += quantity;
        price += productPrice * quantity;
    });
    totalCount.textContent = count;
    totalPrice.textContent = price;
}


async function saveQuantity(productId, quantity) {
    const response = await fetch(
        `https://restaurant-html-production.up.railway.app/cart/${productId}?quantity=${quantity}`,
        {
            method: "POST"
        }
    );
    if (!response.ok) {
        console.log("ошибк");
    }
}
async function loadCart() {
    const response = await fetch(
        "https://restaurant-html-production.up.railway.app/cart"
    );
    const cart = await response.json();
    products.forEach(product => {
        const id = Number(product.dataset.id);
        const item = cart.find(
            item => item.product_id === id
        );
        product.querySelector(".count").textContent =
            item ? item.quantity : 0;
    });

    updateCart();
}


products.forEach(product => {
    const productId = Number(product.dataset.id);

    const plus = product.querySelector(".plus");
    const minus = product.querySelector(".minus");
    const count = product.querySelector(".count");

    plus.addEventListener("click", async () => {
        const newCount = Number(count.textContent) + 1;
        count.textContent = newCount;
        updateCart();
        console.log("push ", productId, newCount);
        await saveQuantity(productId, newCount);
    });

    minus.addEventListener("click", async () => {
        const currentCount = Number(count.textContent);
        if (currentCount > 0) {
            const newCount = currentCount - 1;
            count.textContent = newCount;
            updateCart();
            console.log("push ", productId, newCount);
            await saveQuantity(productId, newCount);
        }
    });
});

document.getElementById("order").addEventListener("click", event => {
    event.preventDefault();
    alert(
        `Заказ оформлен!\nТоваров: ${totalCount.textContent}\nСумма: ${totalPrice.textContent}$`
    );
});

