function getBondYieldByCountry(country) {
  var url = "https://api.tradingeconomics.com/markets/bonds?c=guest:guest"; // Guest access URL

  try {
    // Fetch the data from the Trading Economics API
    var response = UrlFetchApp.fetch(url);
    var data = JSON.parse(response.getContentText());
    
    // Loop through the API response to find the 15Y bond yield for the specified country
    for (var i = 0; i < data.length; i++) {
      var bond = data[i];
      if (bond.Country === country && bond.Name.includes('15Y')) {
        var bondYield = bond.Last;
        return bondYield / 100;  // Return the bond yield as a percentage (divided by 100)
      }
    }
    
    // If no bond yield found for the country, return an error message
    return "Error: No 15Y bond yield found for " + country;
  } catch (e) {
    return "Error fetching bond yield: " + e.message;
  }
}