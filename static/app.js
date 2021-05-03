"use strict";
const API_BASE_URL = 'http://localhost:5000/api';
const $CUPCAKE_LIST = $('#cupcake_list');


async function getCupcakes() {
  console.log('getCupcakes ran')
  let response = await axios.get(`${API_BASE_URL}/cupcakes`)

  let cupcakes = response.data.cupcakes;

  showCupcakeList(cupcakes)

}

function showCupcakeList(cupcakes) {
  console.log('showCupcakeList ran')
  for (let cupcake of cupcakes) {
    let flavor = cupcake.flavor
    let image = cupcake.image
    let rating = cupcake.rating
    let size = cupcake.size

    let $cupcake = $('<li>')
    let cardHTML = `<div class="card" style="width: 18rem;">
    <img class="card-img-top" src="${image}" alt="Card image cap">
    <div class="card-body">
      <h5 class="card-title">${flavor} Cupcake</h5>
      <p class="card-text">Rating: ${rating} Size: ${size}</p>
      <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
  </div>`

    $cupcake.html(cardHTML);
    $CUPCAKE_LIST.append($cupcake);
  }
}

getCupcakes()