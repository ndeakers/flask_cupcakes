"use strict";
const API_BASE_URL = 'http://localhost:5000/api';

// const $jqueryNames
const $CUPCAKE_LIST = $('#cupcake_list');
const $ADD_CUPCAKE_FORM = $('#add_cupcake_form');

/* API request of a list of cupcake objects and show cupcake list */
async function getCupcakes() {
  console.log('getCupcakes ran')
  let response = await axios.get(`${API_BASE_URL}/cupcakes`)

  let cupcakes = response.data.cupcakes;

  showCupcakeList(cupcakes)

}

/*Add individual cupcake list item to HTML*/
function addCupcakeToHTMLList(cupcake) {
  let flavor = cupcake.flavor;
    let image = cupcake.image;
    let rating = cupcake.rating;
    let size = cupcake.size;

    let $cupcake = $('<li>');
    let cardHTML = `<div class="card" style="width: 18rem;">
      <img class="card-img-top" src="${image}" alt="Card image cap">
        <div class="card-body">
          <h5 class="card-title">${flavor} Cupcake</h5>
          <p class="card-text">Rating: ${rating} Size: ${size}</p>
        </div>
      </div>`;

    $cupcake.html(cardHTML);
    $CUPCAKE_LIST.append($cupcake);
}

/*show whole cupcake list on start*/
function showCupcakeList(cupcakes) {
  console.log('showCupcakeList ran')
  for (let cupcake of cupcakes) {
    addCupcakeToHTMLList(cupcake)
  }
}

/*grab values from add form, return as
{flavor, size, rating, image}
marshall
*/
function getFormValues() {
  console.log('getFormValues()')

  let request = {};
  request["flavor"] = $('#flavor_input').val();
  //is a string but is coerced to int
  request["rating"] = $('#rating_input').val();
  request["size"] = $('#size_input').val();
  //TODO fix image! REVIEW THIS
  request["image"] = $('#image_input').val()
    // ? 'https://tinyurl.com/demo-cupcake'
    // : $('#image_input').val()

  console.log('getformValues() -->', request)
  return request
}


/*
Handle add form, post to /cupcakes and add response values as a new cupcake list item to HTML*/
async function addFormHandler(e) {
  e.preventDefault();

  let values = getFormValues();

  let response = await axios.post(`${API_BASE_URL}/cupcakes`, values)
  console.log('cupcake added')

  let addedCupcake = response.data["cupcake"]
  addCupcakeToList(addedCupcake)
}

$ADD_CUPCAKE_FORM.on("submit", addFormHandler);
getCupcakes();