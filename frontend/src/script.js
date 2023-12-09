//import Chart from 'https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js';
import Chart from 'chart.js/auto'

var xhr = null;
//This adds an event listener to all of my tiles
var selectedTile = new Array();
const tickerGraph = document.getElementById('ticker-graph');
var tickerToSearch = "";


document.addEventListener('DOMContentLoaded', function() {
    const tileList = document.querySelectorAll(".tile");
    tileList.forEach(function (tile) {
    
        tile.addEventListener("click", function () {
            if (tile.style.backgroundColor == 'lightblue') {
                tile.style.backgroundColor = 'white';
            } else {
                //Deselect any other tile.
                tileList.forEach(function (tile) {
                    tile.style.backgroundColor = 'white';
                })
                //select current tile
                tile.style.backgroundColor = 'lightblue';
                //do the searchticker thing and empty search bar just in case
                document.getElementById('ticker-search').value = "";
                tickerToSearch = tile.firstElementChild.textContent;
                searchTicker(tickerToSearch);
            }
        })
    });
    
    document.getElementById("ticker-search").addEventListener("keyup", function (event) {
        if (event.keyCode == 13) {
            searchTicker();
        }
    });
})


getXmlHttpRequestObject = function () {
    if (!xhr) {
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

window.onload = function () {
    //loadHistory();
    loadTopPerformers();
};


function loadTPCallBack() {
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Load response received.");
        //historyDiv = document.getElementById('history-container');
        //historyDiv.innerHTML = xhr.responseText;
        console.log(`Data returned: ${xhr.responseText}`);
        
        //Turn the string back into JSON
        const content = JSON.parse(xhr.responseText);
        console.log(content[0].ticker);

        var tileOne = document.getElementById('best-performer-1');
        tileOne.innerHTML = `<h3 id="ticker-one">${content[0].ticker}</h3>
                            <p>Price: $${content[0].price}</p>
                            <p>Change Percentage: ${content[0].change_percentage}</p>
                            <p>Volume: ${content[0].volume}</p>`;
        
        var tileTwo = document.getElementById('best-performer-2');
        tileTwo.innerHTML = `<h3 id="ticker-two">${content[1].ticker}</h3>
                            <p>Price: $${content[1].price}</p>
                            <p>Change Percentage: ${content[1].change_percentage}</p>
                            <p>Volume: ${content[1].volume}</p>`;  
        var tileThree = document.getElementById('best-performer-3');
        tileThree.innerHTML = `<h3 id="ticker-three">${content[2].ticker}</h3>
                            <p>Price: $${content[2].price}</p>
                            <p>Change Percentage: ${content[2].change_percentage}</p>
                            <p>Volume: ${content[2].volume}</p>`; 
        var tileFour = document.getElementById('best-performer-4');
        tileFour.innerHTML = `<h3 id="ticker-four">${content[3].ticker}</h3>
                            <p>Price: $${content[3].price}</p>
                            <p>Change Percentage: ${content[3].change_percentage}</p>
                            <p>Volume: ${content[3].volume}</p>`;      
    }
};

function loadTopPerformers() {
    console.log("Loading user search history...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = loadTPCallBack;

    //Asynchronous request
    xhr.open("GET", "http://localhost:6969/", true);
    xhr.send(null);
};

function searchTickerCallback() {
    console.log("We are in the callback");
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Search response received.");
        
        //The response text here is the graph data currently
        const some_data = JSON.parse(xhr.responseText);
        //console.log(some_data);
        var xValues = new Array();
        var yValues = new Array();
        var aggData = {};

        //Separate aggregate data from graph values
        for (const key in some_data) {
            if(some_data.hasOwnProperty(key)){
                //console.log(`${key} : ${some_data[key]}`);
                if(key == "Average"){
                    aggData["Average"] = some_data[key];
                }else if(key == "Max"){
                    aggData["Max"] = some_data[key];
                }else if(key == "Min"){
                    aggData["Min"] = some_data[key];
                }else {
                    xValues.push(key);
                    yValues.push(some_data[key]);
                }
            }
        }

        //Create graph using values
        var myChart = Chart.getChart(tickerGraph);
        if(myChart != undefined){
            myChart.destroy();
        }

         myChart = new Chart(tickerGraph, {
            type: "line",
            data: {
              labels: xValues,
              datasets: [{
                label: `${tickerToSearch} Close Prices`,
                backgroundColor:"rgba(0,0,255,1.0)",
                borderColor: "rgba(0,0,255,0.1)",
                data: yValues
              }]
            }
          });
          console.log("Drawing graph!");
          myChart.update();

          //Do something with the aggregate data
          var extraInfo = document.getElementById('aggregate-data');
          console.log(aggData);
          extraInfo.innerHTML = `<h4>Aggregate Data: </h4>
                                    <p>Min: $${aggData.Min}</p>
                                    <p>Max: $${aggData.Max}</p>
                                    <p>Average: $${aggData.Average}</p>`;
    }
}

function searchTicker(tileTicker) {
    
    if (!tickerToSearch) { 
        if(!tileTicker){
            console.log("No ticker entered.");
            return;
        }else{
            tickerToSearch = tileTicker;
        }
    }

    console.log("Searching ticker " + tickerToSearch);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = searchTickerCallback;

    //Asynchronous request
    xhr.open("POST", "http://localhost:6969/", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ "data": tickerToSearch }));
}

const submitButton = document.getElementById('submit-button');

submitButton.onclick = function(){
    //We should set all tiles to white when button is clicked.
    const tileList = document.querySelectorAll(".tile");
    tileList.forEach(function(tile){
        if(tile.style.backgroundColor == 'lightblue'){
            tile.style.backgroundColor = 'white';
        }
    });

    tickerToSearch = document.getElementById('ticker-search').value;
    searchTicker(tickerToSearch);
};