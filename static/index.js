
const getRestaurants = async () => {
  //Gets restaurants in selected city
  const url = "http://localhost:5000/api/restaurants"
  const response = await fetch(url)

  return response
}

const getCityLocation = async () => {
  //Gets restaurants in selected city
  const url = "http://localhost:5000/api/location"
  const response = await fetch(url)

  return response
}

async function initMap () {
  const restaurants = await (await getRestaurants()).json()
  const myLatLng = await (await getCityLocation()).json()   // { lat: 60.1699, lng: 24.9384 };

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: myLatLng,
  })

  let markers = []
  for (let index = 0; index < restaurants.length; index++) {
    markers[index] = new google.maps.Marker({
      position: restaurants[index].location,
      map,
      title: restaurants[index].name,
      })
      
      markers[index].addListener("click", () => {
        map.setZoom(16);
        map.setCenter(markers[index].getPosition());
      })
    
  }
}