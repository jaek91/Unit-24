BASE_URL = "http://127.0.0.1:5000/api";

/*create html for cupcakes*/

function createCupcakeHTML(cupcake) {
    return `
    <div data-cupcake-id=${cupcake.id}>
        <li> ${cupcake.flavor} , ${cupcake.size}, ${cupcake.rating} 
            <button id="delete-button">X</button>
        </li>
        <img id="cupcake-img", src=${cupcake.image}, alt="No image available">
    </div>`;

}

/*display initial list of cupcakes*/
async function getCupcakeData() {
    response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let data of response.data.cupcakes) {
        let cupcake = $(createCupcakeHTML(data));
        $("#cupcakes-list").append(cupcake);
    }
}

/*handle submitting of form to update cupcake list*/
$("#cupcake-form").on("submit", async function(evt){
    evt.preventDefault();
    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image =$("#image").val();

    const response = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, size, rating, image
    }) 

    let new_cupcake = $(createCupcakeHTML(response.data.cupcake));
    $("#cupcakes-list").append(new_cupcake)
    $("#cupcake-form").trigger("reset")
})

$("#cupcakes-list").on("click", "#delete-button", async function(evt){
    evt.preventDefault();
    let $selectedCupcake = $(evt.target).closest("div");
    console.log("We came in the delete loop");
    let cupcakeId = $selectedCupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $selectedCupcake.trigger("remove").remove();
});

$(getCupcakeData)