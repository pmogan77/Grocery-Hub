async function sender(e){
    e.preventDefault();

    var name = document.getElementById("Name").value;
    var type = document.getElementById("Type").value;
    var manu = document.getElementById("Manu").value;
    var date = document.getElementById("Date").value;
    var store = "HEB";
    var zip = 78705;
    var price = document.getElementById("Price").value;
    var quantity = document.getElementById("Quantity").value;

    // date: we need it to be 
    var holder = {"product_name": name, "store_name": store, "product_manufacturer":manu, "product_type":type, "zip_code": zip, "quantity": quantity, "discounted_price":price, "expiration_date":date}
    console.log(holder)
    fetch("/add_delete_item",
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