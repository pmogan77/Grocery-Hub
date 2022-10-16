function getProducts() {
    fetch('http://localhost:5003/get_inventory_admin/'+JSON.stringify({zip: 78705}), {method: 'GET'})
                    .then(res => {
                        //res.text().then(res => 
                        //console.log(res))
                        console.log(res["discounted_price"])
                    })
                    .catch(err => console.log(err))
}