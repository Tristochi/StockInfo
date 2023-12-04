var xhr = null;

//This adds an event listener to all of my tiles
var selectedTile = new Array();

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
            }
        })
    });
    
    document.getElementById("ticker-search").addEventListener("keyup", function (event) {
        if (event.keyCode == 13) {
            searchTicker()
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
    loadHistory();
};

function loadHistoryCallback() {
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Load response received.");
        historyDiv = document.getElementById('history-container');
        historyDiv.innerHTML = xhr.responseText;
    }
};

function loadHistory() {
    console.log("Loading user search history...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = loadHistoryCallback;

    //Asynchronous request
    xhr.open("GET", "http://localhost:6969/", true);
    xhr.send(null);
};

function searchTickerCallback() {
    console.log("We are in the callback");
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Search response received.");
        resultDiv = document.getElementById('result-container');
        resultDiv.innerHTML = `<p>${xhr.responseText}</p>`;
    }
}

function searchTicker() {
    tickerToSearch = document.getElementById('ticker-search').value;
    if (!tickerToSearch) {
        console.log("No ticker entered.");
        return;
    }
    console.log("Searching ticker " + tickerToSearch);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = searchTickerCallback;

    //Asynchronous request
    xhr.open("POST", "http://localhost:6969/", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ "data": tickerToSearch }));
}
