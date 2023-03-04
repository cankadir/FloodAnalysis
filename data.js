
function barChart( data ){

    //jpg-export
    var container = document.getElementById('jpg-export')
    
    var bar_container = document.getElementById('bar-chart')
    var chart_height = bar_container.offsetHeight;
    var chart_width = bar_container.offsetWidth;

    console.log( chart_height, chart_width )
    
    // ---- Process Data ----
    // -- Group by
    var result = _.countBy(data, 'agency');

    // -- Extract Values from Object
    let x_values = Object.keys( result );
    let y_values = Object.values( result );

    // ---- PLOT ----
    var plot_data = {
            alignmentgroup: "True",
            hovertemplate: "agency= %{x}<br># of Complaints= %{y}<extra></extra>",
            legendgroup: "0",
            marker: { color: "crimson" },
            name: "0",
            offsetgroup: "0",
            orientation: "v",
            showlegend: false,
            textposition: "auto",
            x: x_values,
            y: y_values,
            type: "bar" 
        }
        
    var plot_layout = {
        template: {
            layout: {
            autotypenumbers: "strict",
            font: { color: "#333333" },
            hovermode: "closest",
            hoverlabel: { align: "left" },
            paper_bgcolor: "white",
            plot_bgcolor: "white",
            xaxis: {
                gridcolor: "#333333",
                linecolor: "#333333",
                ticks: "",
                title: { standoff: 15 },
                zerolinecolor: "white",
                automargin: true,
                zerolinewidth: 2,
            },
            yaxis: {
                ticklabelposition: "outside top",
                gridcolor: "#333333",
                linecolor: "#333333",
                ticks: "",
                title: { standoff: 15 },
                zerolinecolor: "#333333",
                automargin: true,
                zerolinewidth: 2,
            },
            title: { x: 0.05 },
            },
        },
        xaxis: { anchor: "y", domain: [0.0, 1.0], title: { text: "Agency" } },
        yaxis: { anchor: "x", domain: [0.0, 1.0], title: { text: "# of Complaints" } },
        margin: { t: 0 },
        barmode: "relative",
        }

    var config = { responsive: true , displayModeBar: false }

    // Plot chart.
    Plotly.newPlot( "bar-chart", [plot_data], plot_layout, config )
    //Static Image Geenration
    // 1. save plot as image 
    .then((gd) => {
        return Plotly.toImage(gd, { format: 'svg',height:chart_height,width: chart_width });
      })
    //2. Load the svg into the image
    .then((dataURI) => {
        container.setAttribute('src',dataURI);
        container.setAttribute('width',`${chart_width}px`);
        container.setAttribute('height',`${chart_height}px`)
        bar_container.setAttribute('hidden',true)
      });





}

function heatMap(data){

    // ---- Process Data ----
    // -- Get unique Values for Y values
    var descriptors = Object.keys( _.groupBy(data, 'descriptor') );

    // Create weekly data
    let all_weeks = []
    descriptors.forEach(descriptor => { // Filter data by descriptor
        let filtered_data = _.filter(data, function(d){return d.descriptor==descriptor});
        let weekly_data = _.countBy(filtered_data, (dt) => moment(dt.created_date).week() );
        all_weeks.push( weekly_data )
    });

    // find all weeks min/max -> use to to fill missing weeks. 
    let nums = []
    all_weeks.forEach(el => {
        let week_names = Object.keys( el )
        nums.push( week_names.map(Number) )
    });
    
    // min max week number
    let min_week = _.min( nums.flat() )
    let max_week = _.max( nums.flat() )

    let all_values = [];
    all_weeks.forEach(el => {

        // Go over each week from min to max
        // Assign 0 values to non existing weeks
        let in_weeks = Object.keys( el ).map(Number)
        let vals = []
        for( let i=1;i<max_week+1;i++){
            if( in_weeks.includes(i) ){
                vals.push( el[i] )
            }else{
                vals.push( 0 )
            }
        }
        all_values.push( vals )

    });

    let week_values = Array(max_week).fill(min_week).map( (_, i) => i+1 )

    let week_dates = []
    week_values.forEach(week_code => {
        week_dates.push( new Date( moment('2022').add(week_code, 'weeks').startOf('isoweek') ) );
    });

    window.PLOTLYENV = window.PLOTLYENV || {};
    if (document.getElementById("heatmap")) {
    Plotly.newPlot(
        "heatmap",
        [
        {
            coloraxis: "coloraxis",
            x: week_dates,
            y: descriptors,
            z: all_values,
            type: "heatmap",
            xaxis: "x",
            yaxis: "y",
            hovertemplate: "# of Complaints: %{z}<extra></extra>",
        },
        ],
        {
        template: {
                data: {
                heatmap: [
                    {
                    type: "heatmap",
                    colorbar: { outlinewidth: 0 },
                    colorscale: [
                        [0.0, "white"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    },
                ],
                },
                layout: {
                    autotypenumbers: "strict",
                    font: { color: "#333333" },
                    hovermode: "closest",
                    hoverlabel: { align: "left" },
                    paper_bgcolor: "white",
                    plot_bgcolor: "white",
                    coloraxis: { 
                        colorbar: { outlinewidth: 0 },
                        colorscale: [
                            [0.0, "rgb(255,247,236)"],
                            [0.125, "rgb(254,232,200)"],
                            [0.25, "rgb(253,212,158)"],
                            [0.375, "rgb(253,187,132)"],
                            [0.5, "rgb(252,141,89)"],
                            [0.625, "rgb(239,101,72)"],
                            [0.75, "rgb(215,48,31)"],
                            [0.875, "rgb(179,0,0)"],
                            [1.0, "rgb(127,0,0)"],
                        ] 
                    },
                    xaxis: {
                        gridcolor: "white",
                        linecolor: "white",
                        ticks: "",
                        zerolinecolor: "white",
                        automargin: true,
                        zerolinewidth: 2,
                    },
                    yaxis: {
                        gridcolor: "white",
                        linecolor: "white",
                        zerolinecolor: "white",
                        automargin: true,
                        zerolinewidth: 2,
                    },
                    scene: {
                        xaxis: {
                            backgroundcolor: "#E5ECF6",
                            gridcolor: "white",
                            linecolor: "white",
                            showbackground: true,
                            ticks: "",
                            zerolinecolor: "white",
                            gridwidth: 2,
                        },
                        yaxis: {
                            backgroundcolor: "#E5ECF6",
                            gridcolor: "white",
                            linecolor: "white",
                            showbackground: true,
                            ticks: "",
                            zerolinecolor: "white",
                            gridwidth: 2,
                        },
                        zaxis: {
                            backgroundcolor: "#E5ECF6",
                            gridcolor: "white",
                            linecolor: "white",
                            showbackground: true,
                            ticks: "",
                            zerolinecolor: "white",
                            gridwidth: 2,
                        },
                    },
                },
            },
            margin: { t: 0 },
        },
        { responsive: true , displayModeBar:false }
    );
    }
}

// Get Data from URL
let url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json?$where=created_date>='2022-01-01' AND within_circle(location, 40.6575627, -73.840941, 1609) AND (descriptor='Street Flooding (SJ)' OR descriptor='Catch Basin Clogged/Flooding (Use Comments) (SC)' OR descriptor='Sewer Backup (Use Comments) (SA)' OR descriptor='Failure To Retain Water/Improper Drainage- (LL103/89)' OR descriptor='Manhole Overflow (Use Comments) (SA1)' OR descriptor='Snow/Ice')"

fetch(url)
  .then(response => response.json())
  .then((data) => {

    // Run plot queries. 
    // They go to specific Div's so this is OK. 
    heatMap( data );
    barChart( data );

  });












