// Set the dimensions and margins of the graph.
var margin = { top: 0, right: 0, bottom: 0, left: 200 },
  width = 1000 - margin.left - margin.right,
  height = 600 - margin.top - margin.bottom;

// Append the svg object to the body of the page.
var emptySvg = d3
  .select("#empty-graphic")
  .append("svg")
  .classed("mobile-svg", true)
  .attr("preserveAspectRatio", "xMinYMin meet")
  .attr("viewBox", "0 0 1000 600")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var unadjustedSvg = d3
  .select("#unadjusted-graphic")
  .append("svg")
  .classed("mobile-svg", true)
  .attr("preserveAspectRatio", "xMinYMin meet")
  .attr("viewBox", "0 0 1000 600")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var incrementSvg = d3
  .select("#increment-graphic")
  .append("svg")
  .classed("mobile-svg", true)
  .attr("preserveAspectRatio", "xMinYMin meet")
  .attr("viewBox", "0 0 1000 600")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var adjustedSvg = d3
  .select("#adjusted-graphic")
  .append("svg")
  .classed("mobile-svg", true)
  .attr("preserveAspectRatio", "xMinYMin meet")
  .attr("viewBox", "0 0 1000 600")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var monthlySvg = d3
  .select("#monthly-graphic")
  .append("svg")
  .classed("mobile-svg", true)
  .attr("preserveAspectRatio", "xMinYMin meet")
  .attr("viewBox", "0 0 1000 600")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Gridlines in Y-axis function.
function make_y_gridlines(y) {
  return d3.axisLeft(y).ticks(4).tickValues([25, 50, 75, 100]);
}

// Read the data.
d3.csv("data/data.csv", function (data) {
  // Add X axis --> it is a date format.
  var parseTime = d3.timeParse("%Y-%m-%d");

  var dates = [];
  for (var obj of data) {
    dates.push(parseTime(obj.date));
  }

  var xMobile = d3
    .scaleTime()
    .domain(d3.extent(dates))
    .range([0, width]);

  var yMobile = d3
    .scaleLinear()
    .domain([0, 100])
    .range([height, 100]);

  // Make the chart SVG.
  emptySvg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("class", "mobile-graph")
    .style("font-size", "12px")
    .style("font-family", "Roboto, sans-serif")
    .call(d3.axisBottom(xMobile));

  // Add the Y-axis gridlines.
  emptySvg
    .append("g")
    .attr("stroke-dasharray", "5, 5")
    .attr("opacity", ".4")
    .attr("class", "mobile-graph")
    .call(make_y_gridlines(yMobile).tickSize(-width).tickFormat(""))
    .call((g) => g.select(".domain").remove());

  // Text label for the Y-axis.
  emptySvg
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -height / 2 - 140)
    .attr("dy", "1em")
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "14px")
    .style("font-weight", "700")
    .style("letter-spacing", ".005em")
    .style("fill", backgroundColor)
    .text("AMOUNT OF SEARCHES →");

  // Text label for the title.
  emptySvg
    .append("text")
    .attr("x", 158)
    .attr("y", 0 - margin.top / 2 + 80)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .text("DATA");

  // Text under the graph.
  emptySvg
    .append("line")
    .attr("stroke-width", 0.5)
    .style("stroke", backgroundColor)
    .attr("x1", -20)
    .attr("y1", height + 40)
    .attr("x2", width + 20)
    .attr("y2", height + 40);

  emptySvg
    .append("text")
    .attr("x", -20)
    .attr("y", height + 56)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "9px")
    .style("font-weight", "300")
    .text(
      "The line indicates the relative amount of searches over the timespan 2004—2020. All data is collected from trends.google.com, and modifications were made where needed."
    );

  // The line.
  emptySvg
    .append("g")
    .append("g")
    .append("path")
    .datum(data)
    .attr(
      "d",
      d3
        .line()
        .x(function (d) {
          return xMobile(+parseTime(d.date));
        })
        .y(function (d) {
          return yMobile(+d.start);
        })
    )
    .attr("stroke", backgroundColor)
    .style("stroke-width", 1)
    .style("fill", "none");

    // Make the chart SVG.
  unadjustedSvg
  .append("g")
  .attr("transform", "translate(0," + height + ")")
  .attr("class", "mobile-graph")
  .style("font-size", "12px")
  .style("font-family", "Roboto, sans-serif")
  .call(d3.axisBottom(xMobile));

  // Add the Y-axis gridlines.
  unadjustedSvg
    .append("g")
    .attr("stroke-dasharray", "5, 5")
    .attr("opacity", ".4")
    .attr("class", "mobile-graph")
    .call(make_y_gridlines(yMobile).tickSize(-width).tickFormat(""))
    .call((g) => g.select(".domain").remove());

  // Text label for the Y-axis.
  unadjustedSvg
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -height / 2 - 140)
    .attr("dy", "1em")
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "14px")
    .style("font-weight", "700")
    .style("letter-spacing", ".005em")
    .style("fill", "#E9D758")
    .text("AMOUNT OF SEARCHES →");

  // Text label for the title.
  unadjustedSvg
    .append("text")
    .attr("x", 158)
    .attr("y", 0 - margin.top / 2 + 80)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .text("DATA");

  unadjustedSvg
    .append("text")
    .attr("x", 152)
    .attr("y", -(margin.top / 2) + 80)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .style("text-anchor", "end")
    .style("fill", "#E9D758")
    .text("UNADJUSTED");

  // Text under the graph.
  unadjustedSvg
    .append("line")
    .attr("stroke-width", 0.5)
    .style("stroke", backgroundColor)
    .attr("x1", -20)
    .attr("y1", height + 40)
    .attr("x2", width + 20)
    .attr("y2", height + 40);

  unadjustedSvg
    .append("text")
    .attr("x", -20)
    .attr("y", height + 56)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "9px")
    .style("font-weight", "300")
    .text(
      "The line indicates the relative amount of searches over the timespan 2004—2020. All data is collected from trends.google.com, and modifications were made where needed."
    );

  // The line.
  unadjustedSvg
    .append("g")
    .append("g")
    .append("path")
    .datum(data)
    .attr(
      "d",
      d3
        .line()
        .x(function (d) {
          return xMobile(+parseTime(d.date));
        })
        .y(function (d) {
          return yMobile(+d.unadjusted);
        })
    )
    .attr("stroke", "#E9D758")
    .style("stroke-width", 1)
    .style("fill", "none");

  // Make the chart SVG.
  incrementSvg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("class", "mobile-graph")
    .style("font-size", "12px")
    .style("font-family", "Roboto, sans-serif")
    .call(d3.axisBottom(xMobile));

  // Text label for the Y-axis.
  incrementSvg
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -height / 2 - 140)
    .attr("dy", "1em")
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "14px")
    .style("font-weight", "700")
    .style("letter-spacing", ".005em")
    .style("fill", "#E9D758")
    .text("AMOUNT OF SEARCHES →");

  // Text label for the title.
  incrementSvg
    .append("text")
    .attr("x", 158)
    .attr("y", 0 - margin.top / 2 + 80)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .text("DATA");

  incrementSvg
    .append("text")
    .attr("x", 152)
    .attr("y", -(margin.top / 2) + 80)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .style("text-anchor", "end")
    .style("fill", "#E9D758")
    .text("UNADJUSTED");

  // Text under the graph.
  incrementSvg
    .append("line")
    .attr("stroke-width", 0.5)
    .style("stroke", backgroundColor)
    .attr("x1", -20)
    .attr("y1", height + 40)
    .attr("x2", width + 20)
    .attr("y2", height + 40);

  incrementSvg
    .append("text")
    .attr("x", -20)
    .attr("y", height + 56)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "9px")
    .style("font-weight", "300")
    .text(
      "The line indicates the relative amount of searches over the timespan 2004—2020. All data is collected from trends.google.com, and modifications were made where needed."
    );

  // The line.
  incrementSvg
    .append("g")
    .append("g")
    .append("path")
    .datum(data)
    .attr(
      "d",
      d3
        .line()
        .x(function (d) {
          return xMobile(+parseTime(d.date));
        })
        .y(function (d) {
          return yMobile(+d.unadjusted);
        })
    )
    .attr("stroke", "#E9D758")
    .style("stroke-width", 1)
    .style("fill", "none");

    incrementSvg
    .append("g")
      .attr("opacity", 0.4)
      .attr("transform", "translate(0," + height + ")")
      .call(
        d3
          .axisBottom(xMobile)
          .ticks(d3.timeMonth.every(6))
          .tickFormat("")
          .tickSize(-height + 100)
      )
      .selectAll("line")
      .attr("stroke", backgroundColor);

  // Make the chart SVG.
  adjustedSvg
  .append("g")
  .attr("transform", "translate(0," + height + ")")
  .attr("class", "mobile-graph")
  .style("font-size", "12px")
  .style("font-family", "Roboto, sans-serif")
  .call(d3.axisBottom(xMobile));

  // Add the Y-axis gridlines.
  adjustedSvg
    .append("g")
    .attr("stroke-dasharray", "5, 5")
    .attr("opacity", ".4")
    .attr("class", "mobile-graph")
    .call(make_y_gridlines(yMobile).tickSize(-width).tickFormat(""))
    .call((g) => g.select(".domain").remove());

  // Text label for the Y-axis.
  adjustedSvg
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -height / 2 - 140)
    .attr("dy", "1em")
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "14px")
    .style("font-weight", "700")
    .style("letter-spacing", ".005em")
    .style("fill", "#48E5C2")
    .text("AMOUNT OF SEARCHES →");

  // Text label for the title.
  adjustedSvg
    .append("text")
    .attr("x", 158)
    .attr("y", 0 - margin.top / 2 + 80)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .text("DATA");

  adjustedSvg
    .append("text")
    .attr("x", 152)
    .attr("y", -(margin.top / 2) + 80)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .style("text-anchor", "end")
    .style("fill", "#48E5C2")
    .text("ADJUSTED");

  // Text under the graph.
  adjustedSvg
    .append("line")
    .attr("stroke-width", 0.5)
    .style("stroke", backgroundColor)
    .attr("x1", -20)
    .attr("y1", height + 40)
    .attr("x2", width + 20)
    .attr("y2", height + 40);

  adjustedSvg
    .append("text")
    .attr("x", -20)
    .attr("y", height + 56)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "9px")
    .style("font-weight", "300")
    .text(
      "The line indicates the relative amount of searches over the timespan 2004—2020. All data is collected from trends.google.com, and modifications were made where needed."
    );

  // The line.
  adjustedSvg
    .append("g")
    .append("g")
    .append("path")
    .datum(data)
    .attr(
      "d",
      d3
        .line()
        .x(function (d) {
          return xMobile(+parseTime(d.date));
        })
        .y(function (d) {
          return yMobile(+d.normalised);
        })
    )
    .attr("stroke", "#48E5C2")
    .style("stroke-width", 1)
    .style("fill", "none");

  // Make the chart SVG.
  monthlySvg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("class", "mobile-graph")
    .style("font-size", "12px")
    .style("font-family", "Roboto, sans-serif")
    .call(d3.axisBottom(xMobile));

  // Add the Y-axis gridlines.
  monthlySvg
    .append("g")
    .attr("stroke-dasharray", "5, 5")
    .attr("opacity", ".4")
    .attr("class", "mobile-graph")
    .call(make_y_gridlines(yMobile).tickSize(-width).tickFormat(""))
    .call((g) => g.select(".domain").remove());

  // Text label for the Y-axis.
  monthlySvg
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -height / 2 - 140)
    .attr("dy", "1em")
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "14px")
    .style("font-weight", "700")
    .style("letter-spacing", ".005em")
    .style("fill", "71A9F7")
    .text("AMOUNT OF SEARCHES →");

  // Text label for the title.
  monthlySvg
    .append("text")
    .attr("x", 158)
    .attr("y", 0 - margin.top / 2 + 80)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .text("DATA");

  monthlySvg
    .append("text")
    .attr("x", 152)
    .attr("y", -(margin.top / 2) + 80)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .style("text-anchor", "end")
    .style("fill", "#71A9F7")
    .text("MONTHLY");

  // Text under the graph.
  monthlySvg
    .append("line")
    .attr("stroke-width", 0.5)
    .style("stroke", backgroundColor)
    .attr("x1", -20)
    .attr("y1", height + 40)
    .attr("x2", width + 20)
    .attr("y2", height + 40);

  monthlySvg
    .append("text")
    .attr("x", -20)
    .attr("y", height + 56)
    .style("fill", backgroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "9px")
    .style("font-weight", "300")
    .text(
      "The line indicates the relative amount of searches over the timespan 2004—2020. All data is collected from trends.google.com, and modifications were made where needed."
    );

  // The line.
  monthlySvg
    .append("g")
    .append("path")
    .datum(data)
    .attr(
      "d",
      d3
        .line()
        .x(function (d) {
          return xMobile(+parseTime(d.date));
        })
        .y(function (d) {
          return yMobile(+d.normalised);
        })
    )
    .attr("stroke", "#48E5C2")
    .style("stroke-width", 1)
    .style("fill", "none");

  monthlySvg
    .append("g")
    .append("path")
    .datum(data)
    .attr(
      "d",
      d3
        .line()
        .x(function (d) {
          return xMobile(+parseTime(d.date));
        })
        .y(function (d) {
          return yMobile(+d.monthly);
        })
    )
    .attr("stroke", "#71A9F7")
    .style("stroke-width", 1)
    .style("fill", "none");

});
