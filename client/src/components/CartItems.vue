<template>
    <NotLoggedInMessage v-if="!isAuthenticated" />
    <div class="no-items" v-if="plates.length === 0"> There are no items in the cart. </div>
    <div class="p-grid">
    <div class="p-col-12 p-md-6" v-for="plate in plates" :key="plate.id">
      <div class="p-card p-shadow-2">
        <div class="p-card-content">
          <div class="p-card-flex">
             <button @click="removePlate(plate)" class="p-button p-button-icon p-button-danger p-button-xs custom-remove-button">
               <i class="pi pi-times"></i>
             </button>
            <div class="p-card-image">
              <img :src="plate.picture" :alt="plate.plate_name" class="p-card-image" />
            </div>
            <div class="p-card-details">
              <div class="p-card-header p-card-flex">
                <div class="p-card-title">{{ plate.plate_name }} x {{ plate.shopping_cart[0].plate_quantity }}</div>
                <div class="p-card-subtitle"> = {{ plate.price * plate.shopping_cart[0].plate_quantity }} €</div>
              </div>
            </div>
            <div class="p-card-quantity-buttons">
              <div class="p-button-container">
                <button @click="incrementQuantity(plate)" class="p-button p-button-icon p-button-primary">
                  <i class="pi pi-plus p-icon-small"></i>
                </button>
              </div>
              <div class="p-button-container">
                <button @click="decrementQuantity(plate)" class="p-button p-button-icon p-button-danger">
                  <i class="pi pi-minus p-icon-small"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="plates.length > 0">
      <div class="p-col-12">
        <div class="p-card p-shadow-2">
          <div class="p-card-content">
            <div class="p-card-total">
              Total Price: {{ calculateTotalPrice() }} €
            </div>
          </div>
        </div>
      </div>

      <div class="p-col-12">
        <button class="p-button p-button-primary p-button-lg" @click="placeOrder">Place Order</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';

const { isAuthenticated } = defineProps(['isAuthenticated']);
const plates = ref([]);
const userId = localStorage.getItem('userId');

onMounted(async () => {
  const response = await fetch(`/api/cart-items/items/${userId}`);
  const data = await response.json();
  plates.value = data;
});

function calculateTotalPrice() {
  return plates.value.reduce((total, plate) => {
    return total + plate.price * plate.shopping_cart[0].plate_quantity;
  }, 0).toFixed(2);
}

// Removing item from cart
async function removePlate(plate) {
  const plateName = plate.plate_name

  try {
    const response = await fetch(`/api/cart-items/remove/${plate.plate_id}/${userId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      window.location.reload();
    } else {
      alert("Failed to remove " + plateName + " from cart.");
    }
  } catch (error) {
    alert("An error occurred while removing " + plateName + " from cart.");
  }
}

// Placing order from cart
async function placeOrder() {
	const cartItemsResponse = await fetch(`/api/cart-items/${userId}`);
    const cartItemsData = await cartItemsResponse.json();

  try {
    const response = await fetch(`/api/orders/add-new-order/${userId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(cartItemsData),
    });

    if (response.ok) {
      alert("Order placed successfully 🥘");
      window.location.reload();
    } else {
      alert("Failed to place order. Please try again after some time.");
    }
  } catch (error) {
    alert("An error occurred while placing order.");
  }
}


// Increasing pkate quantity
async function incrementQuantity(plate) {
  const updatedQuantity = plate.shopping_cart[0].plate_quantity + 1;
  await updateQuantity(plate, updatedQuantity);
}

// Decreasing plate quantity
async function decrementQuantity(plate) {
  const updatedQuantity = plate.shopping_cart[0].plate_quantity - 1;
  await updateQuantity(plate, updatedQuantity);
}

// Updating the plate quantity
async function updateQuantity(plate, updatedQuantity) {
  const plateName = plate.plate_name;

  if (updatedQuantity === 0) {
    removePlate(plate)
  }
  else {
    try {
      const response = await fetch(`/api/cart-items/update-quantity/${userId}/${plate.plate_id}?quantity=${updatedQuantity}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        window.location.reload();
      } else {
        alert(`Failed to update ${plateName} quantity`);
      }
    } catch (error) {
      alert(`An error occurred while updating ${plateName} quantity`);
    }
  }
}

</script>

<style scoped>

.p-card-flex {
  display: flex;
  align-items: center;
}

.p-card-content {
  padding: 1.25rem 1rem;
  margin: 10px;
}

.p-card-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.p-card .p-card-title {
  font-size: 20px;
}

.p-card-subtitle {
  text-align: right;
}

.p-card-title, .p-card-subtitle {
  display: inline-block;
  margin-right: 10px;
  font-weight: 700 !important;
}

.p-card-image {
  max-width: 100px;
  margin-right: 25px;
  margin-left: 10px;
  border-radius: 8px;
}

.p-card-flex {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.p-card-total {
  text-align: right;
  font-weight: bold;
  margin-top: 10px;
  margin-right: 10px;
}

.custom-remove-button {
  padding: 0.25rem 0.5rem;
  font-size: 14px;
}

.no-items {
  margin-top: 20px;
  font-size: 20px;
}

.p-button-lg {
  background-color: green;
  margin-top: 10px
}

.p-button-container {
  margin-bottom: 5px;
}

.p-icon-small {
    font-size: 10px;
}
</style>
