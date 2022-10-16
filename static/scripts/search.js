async function sender(e){
    e.preventDefault();

    var zip = document.getElementById("zipcode").value;
    var store = document.getElementById("store").value;
    var food_type = document.getElementById("food_type").value;

    var holder = {"zip": zip, "store": store, "food_type": food_type}
    console.log("hi1")
    fetch("/grocery_search",
    {
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },   
        method: 'POST',
        body: JSON.stringify(holder)
    }).then(res => console.log(res.text()))

    console.log(holder)
}


async function redirect(e){
    e.preventDefault();
    console.log("Testing");
    var zip = document.getElementById("zipcode").value;
    var store = document.getElementById("store").value;
    var food_type = document.getElementById("food_type").value;
    window.location='/community?zip='+zip+'&store='+store+'&food_type='+food_type
}