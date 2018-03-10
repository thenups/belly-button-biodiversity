function renderDropdown() {
    Plotly.d3.json('/names', function(error, data){
        if (error) return console.warn(error);

        selectElem = d3.select('#sampleChoices');

        selectElem.selectAll('option')
            .data(data)
            .enter()
            .append('option')
            .attr('value',function(d){return d;})
            .text(function(d){return d;});
    });
};

function createPieChart(trace, restyle) {

    if (restyle) {
        Plotly.restyle('pie', trace);
    }

    var trace1 = {
        values: trace.values,
        labels: trace.labels,
        text: trace.descriptions,
        type: 'pie'
    }

    var data = [trace1];
    var layout = {
        title: 'Pie Chart'
    };

    Plotly.newPlot('pie',data,layout)
}

function createBubblePlot(trace, restyle) {
    if (restyle) {
        Plotly.restyle('bubble', trace);
    };

    var trace1 = {
        x: trace.x,
        y: trace.y,
        mode: 'markers',
        text: trace.descriptions,
        marker: {
            size: trace.marker.size
            }
    };
    console.log(trace.marker.size);
    var data = [trace1];

    var layout = {
        title: 'Marker Size',
        showlegend: false,
        height: 600,
        width: 600
        };

    Plotly.newPlot('bubble', data, layout);
};

function populateMetadata(sample) {
    metaURL = '/metadata/' + sample
    Plotly.d3.json(metaURL, function(error, data){
        if (error) return console.warn(error);

        var details = new Array;

        for (var key in data) {
            details.push(key+': '+data[key]);
        };

        selectElem = d3.select('#metadataInfo');
        selectElem.html('');
        console.log('CLEAR HTML');
        selectElem.selectAll('p')
            .data(details)
            .enter()
            .append('p')
            .attr('class','metaDetails')
            .text(function(d){return d;});

        console.log('POPULATE');
    });
};

function pullPieData(sample, restyle){
    sampleURL = '/samples/' + sample;

    Plotly.d3.json(sampleURL, function(error, data){
        if (error) return console.warn(error);

        var trace = {
            values: data.sample_values.slice(0,10),
            labels: data.otu_ids.slice(0,10),
            text: data.descriptions.slice(0,10)
        };

        if (restyle) {createPieChart(trace, true);};

        createPieChart(trace);
    });
}

function pullBubbleData(sample, restyle){
    sampleURL = '/samples/' + sample;

    Plotly.d3.json(sampleURL, function(error, data){
        if (error) return console.warn(error);

        var trace = {
            x: data.otu_ids,
            y: data.sample_values,
            marker: {
                size: data.sample_values,
            },
            text: data.descriptions
        }

        if (restyle) {createBubblePlot(trace, true);};

        createBubblePlot(trace);
    });
}

function optionChanged(dataset) {
    pullPieData(dataset,true);
    pullBubbleData(dataset,true);
    populateMetadata(dataset);
};


renderDropdown();
pullPieData('BB_940');
pullBubbleData('BB_940');
populateMetadata('BB_940');
