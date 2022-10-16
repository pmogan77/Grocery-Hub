async function sender(e){
    e.preventDefault();

    var email = document.getElementById("email").value;
    var zip = document.getElementById("zipcode").value;
    var store = document.getElementById("store").value;
    var food = document.getElementById("food_type").value;

    var holder = {"email": email, "zip": zip, "store": store, "food_type": food}
    console.log(holder)
    fetch("/add_to_mail_list",
    {
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },   
        method: 'POST',
        body: JSON.stringify(holder)
    })

    console.log(holder)
}