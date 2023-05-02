function setTemp() {
    fetch(`http://localhost:6543/recent_temp`)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json()
    })
    .then((data) => {
        let tempX = [];
        let tempY = [];
        for(i in data){
            tempX.push(data[i]['time']);
            tempY.push(data[i]['temp']);
        }
        // console.log(tempX);
        // console.log(tempY);
        // tempY = [30, 50, 70, 90, 70, 50, 10, 20]
        var tempTrace = {
            x: tempX,
            y: tempY,
            type: 'scatter'
        };
        Plotly.newPlot('temp', [tempTrace]);
    })
    .catch((error) => {
        console.error(error);
    });
}

function setHum() {
    fetch(`http://localhost:6543/recent_hum`)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json()
    })
    .then((data) => {
        console.log(data);
        let tempX = [];
        let tempY = [];
        for(i in data){
            tempX.push(data[i]['time']);
            tempY.push(data[i]['hum']);
        }
        // console.log(tempX);
        // console.log(tempY);
        // tempY = [0, 0, 10, 6, 32, 12, 2, 10]
        var tempTrace = {
            x: tempX,
            y: tempY,
            type: 'scatter'
        };
        Plotly.newPlot('hum', [tempTrace]);
    })
    .catch((error) => {
        console.error(error);
    });
}

function setLight() {
    fetch(`http://localhost:6543/recent_light`)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json()
    })
    .then((data) => {
        let tempX = [];
        let tempY = [];
        for(i in data){
            tempX.push(data[i]['time']);
            tempY.push(data[i]['light']);
        }
        // tempY = [0, 1, 2, 3, 4, 5, 6, 7]
        var tempTrace = {
            x: tempX,
            y: tempY,
            type: 'scatter'
        };
        Plotly.newPlot('light', [tempTrace]);
    })
    .catch((error) => {
        console.error(error);
    });
}

setTemp();
setHum();
setLight();
setInterval(setTemp, 15000);
setInterval(setHum, 15000);
setInterval(setLight, 15000);

