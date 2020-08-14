// Colour codes.
const foregroundColor = "#f2f3f4";
const backgroundColor = "#131516";

// Set the dimensions and margins of the graph.
var margin = { top: 100, right: 150, bottom: 100, left: 50 },
  width = 800 - margin.left - margin.right,
  height = 600 - margin.top - margin.bottom;

// Append the svg object to the body of the page.
var svg = d3
  .select("#vis0")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Gridlines in Y-axis function.
function make_y_gridlines(y, data) {
  return d3.axisLeft(y).ticks(1).tickValues([data[0].position]);
}

// Read the data.
d3.csv("data/state.csv", function (data) {
  // Convert position to integer, else d3.max() doesn't work.
  data.forEach(function (d) {
    d.position = parseInt(d.position);
  });

  // Add X axis --> it is a date format.
  var parseTime = d3.timeParse("%Y-%m-%d");

  var dates = [];
  for (var obj of data) {
    dates.push(parseTime(obj.date));
  }

  var x = d3.scaleTime().domain(d3.extent(dates)).range([0, width]);

  var y = d3
    .scaleLinear()
    .domain([d3.min(data, (d) => d.position) * 0.75, d3.max(data, (d) => d.position)])
    .range([height, 100]);

  // Make the chart SVG.
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("class", "graph0")
    .style("font-size", "12px")
    .style("font-family", "Roboto, sans-serif")
    .call(d3.axisBottom(x));

  // Add the Y-axis gridlines.
  svg
    .append("g")
    .attr("stroke-dasharray", "5, 5")
    .attr("opacity", ".4")
    .attr("class", "graph0")
    .call(make_y_gridlines(y, data).tickSize(-width).tickFormat(""))
    .call((g) => g.select(".domain").remove());

  // Text label for the Y-axis.
  svg
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - 40)
    .attr("x", 0 - height / 2 - 140)
    .attr("dy", "1em")
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "14px")
    .style("letter-spacing", ".005em")
    .style("fill", foregroundColor)
    .text("POSITION →");

  // Text label for the title.
  svg
    .append("text")
    .attr("x", 0)
    .attr("y", 0 - margin.top / 2 + 100)
    .style("fill", foregroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "20px")
    .style("font-weight", "700")
    .text("CURRENT STATE OF THE ALGORITHM");

  // Text under the graph.
  svg
    .append("line")
    .attr("stroke-width", 0.5)
    .style("stroke", foregroundColor)
    .attr("x1", -20)
    .attr("y1", height + 40)
    .attr("x2", width + 20)
    .attr("y2", height + 40);

  svg
    .append("text")
    .attr("x", -20)
    .attr("y", height + 56)
    .style("fill", foregroundColor)
    .style("font-family", "Roboto, sans-serif")
    .style("font-size", "9px")
    .style("font-weight", "300")
    .text(
      "DJIA stock price data is used as a placeholder for now, because the machine learning model has not been deployed yet."
    );

  // svg
  //   .append("text")
  //   .attr("x", -20)
  //   .attr("y", height + 71)
  //   .style("fill", foregroundColor)
  //   .style("font-family", "Roboto, sans-serif")
  //   .style("font-size", "9px")
  //   .style("font-weight", "300")
  //   .text("the model.");

  // The line.
  svg
    .append("g")
    .append("g")
    .append("path")
    .datum(data)
    .attr(
      "d",
      d3
        .line()
        .x(function (d) {
          return x(+parseTime(d.date));
        })
        .y(function (d) {
          return y(+d.position);
        })
    )
    .attr("stroke", foregroundColor)
    .style("stroke-width", 1)
    .style("fill", "none");

  // The last value at the end of the line.
  const lastValue = data[data.length - 1].position;

  const lineText = svg
    .append("text")
    .style("fill", foregroundColor)
    .style("font-family", "Roboto")
    .style("font-size", "14px")
    .style("opacity", "0")
    .attr("transform", "translate(600," + y(lastValue) + ")")
    .attr("x", 8)
    .attr("y", ".35em")
    .text(lastValue.toFixed(2) + "%");

  // Animate the path via scrolling.
  const path = d3.select("svg g g g path").data([data]);
  const pathLength = path.node().getTotalLength();

  path
    .attr("stroke-dasharray", pathLength + " " + pathLength)
    .attr("stroke-dashoffset", pathLength)
    .attr("position", "fixed");

  const updatePath = (index) => {
    path.attr("stroke-dashoffset", pathLength - index);
  };

  const html = document.documentElement;

  window.addEventListener("scroll", () => {
    const startAnimate = 910;

    var scrollTop = html.scrollTop - startAnimate;

    if (scrollTop < 0) {
      scrollTop = 0;
    }

    const maxScrollTop = 420;
    const scrollFraction = scrollTop / maxScrollTop;

    const startGraphs = 1100;
    const stopGraphs = 4450;

    if (scrollTop > startGraphs) {
      document.getElementById("vis").style.position = "fixed";
      document.getElementById("vis").style.top = "200px";
    } else {
      document.getElementById("vis").style.top = "2214px";
      document.getElementById("vis").style.position = "absolute";
    }

    if (scrollTop > stopGraphs) {
      document.getElementById("vis").style.top = "5562px";
      document.getElementById("vis").style.position = "absolute";
    } else if (scrollTop > startGraphs) {
      document.getElementById("vis").style.top = "200px";
      document.getElementById("vis").style.position = "fixed";
    }

    if (scrollFraction >= 1) {
      lineText.style("opacity", (scrollFraction - 1) * 50);
    } else {
      lineText.style("opacity", "0");
    }

    const pathIndex = Math.min(
      pathLength - 1,
      Math.floor(scrollFraction * pathLength)
    );

    requestAnimationFrame(() => updatePath(pathIndex + 1));
  });
});
