// Success function 
function successFunction(value) { 
    var lat = value.coords.latitude; 
    var long = value.coords.longitude; 
    document.getElementById('error').innerHTML = ""; 

    // Call function to get city and country based on latitude and longitude
    getCityCountry(lat, long);

    document.getElementById('latitude').innerHTML = `Latitude: ${lat}`; 
    document.getElementById('longitude').innerHTML = `Longitude: ${long}`; 
    } 

    // Error Function 
    function errorFunction(err) { 
    document.getElementById('latitude').innerHTML = ""; 
    document.getElementById('longitude').innerHTML = ""; 
    document.getElementById('error').innerHTML = `Error occurred: ${err.message}`; 
    } 

    // Function to get city and country based on latitude and longitude
    async function getCityCountry(lat, long) {
    const apiKey = 'e87943131c884aacad1135735242112'; // Replace with your OpenWeatherMap API key
    const url = `https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${lat},${long}&aqi=yes`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        if (data.location && data.location.name && data.location.country) {
            const city = data.location.name || 'Not available';
            const country = data.location.country || 'Not available';
            document.getElementById('city').innerHTML = `City: ${city}`;
            document.getElementById('country').innerHTML = `Country: ${country}`;
        } else {
            document.getElementById('city').innerHTML = 'City: Not found';
            document.getElementById('country').innerHTML = 'Country: Not found';
        }
    } catch (error) {
        document.getElementById('city').innerHTML = 'City: Error';
        document.getElementById('country').innerHTML = 'Country: Error';
    }
    }

    // Main function to get location 
    function getLocation() { 
    navigator.geolocation.getCurrentPosition(successFunction, errorFunction); 
}