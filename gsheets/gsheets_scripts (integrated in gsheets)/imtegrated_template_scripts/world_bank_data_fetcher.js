/**
 * Returns the inflation rate for a given country.
 * Currently, only Germany is supported for simplicity.
 * 
 * @param {string} country The country name (only "Germany" is supported)
 * @return {number|string} The inflation rate as a decimal (e.g., 0.0523 for 5.23%) or an error message.
 */
function get_inflation_rate(country) {
  // Validate the country input (only Germany is supported)
  if (country !== "Germany") {
    return "Error: Only Germany is supported.";
  }
  
  // World Bank API URL for inflation data
  var inflationUrl = "https://api.worldbank.org/v2/country/DEU/indicator/FP.CPI.TOTL.ZG?format=json";
  
  try {
    // Send GET request to the World Bank API for inflation
    var inflationResponse = UrlFetchApp.fetch(inflationUrl);
    var inflationData = JSON.parse(inflationResponse.getContentText());
    
    // Extract and return the inflation rate as a decimal (e.g., 5.23 -> 0.0523)
    var inflationRate = inflationData[1][0]['value'];
    if (inflationRate !== null) {
      return inflationRate / 100;
    } else {
      return "No inflation data available.";
    }
  } catch (e) {
    return "Error: " + e.message;
  }
}

/**
 * Returns the economic growth rate for a given country.
 * Currently, only Germany is supported for simplicity.
 * 
 * @param {string} country The country name (only "Germany" is supported)
 * @return {number|string} The economic growth rate as a decimal (e.g., 0.025 for 2.5%) or an error message.
 */
function get_economic_growth_rate(country) {
  // Validate the country input (only Germany is supported)
  if (country !== "Germany") {
    return "Error: Only Germany is supported.";
  }
  
  // World Bank API URL for economic growth data
  var growthUrl = "https://api.worldbank.org/v2/country/DEU/indicator/NY.GDP.MKTP.KD.ZG?format=json";
  
  try {
    // Send GET request to the World Bank API for economic growth
    var growthResponse = UrlFetchApp.fetch(growthUrl);
    var growthData = JSON.parse(growthResponse.getContentText());
    
    // Extract and return the economic growth rate as a decimal (e.g., 2.5 -> 0.025)
    var growthRate = growthData[1][0]['value'];
    if (growthRate !== null) {
      return growthRate / 100;
    } else {
      return "No economic growth data available.";
    }
  } catch (e) {
    return "Error: " + e.message;
  }
}

/**
 * Tutorial on how to use these functions.
 *
 * Usage:
 * 1. To get the inflation rate of Germany, use the function:
 *    =get_inflation_rate("Germany")
 *    This will return the inflation rate as a decimal (e.g., 0.0523 for 5.23%).
 *
 * 2. To get the economic growth rate of Germany, use the function:
 *    =get_economic_growth_rate("Germany")
 *    This will return the economic growth rate as a decimal (e.g., 0.025 for 2.5%).
 *
 * Please note that, for simplicity reasons, these functions currently support only Germany.
 */