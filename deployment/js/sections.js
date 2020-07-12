function scrollVis() {
  const margin = { top: 0, left: 150, bottom: 50, right: 100 };
  const width = 1000 - margin.left - margin.right;
  const height = 600 - margin.top - margin.bottom;

  var lastIndex = -1;
  var activeIndex = 0;

  var svg = null;
  var g = null;

  var xAdjustment = d3.scaleTime().range([0, width]);

  var yAdjustment = d3.scaleLinear().domain([0, 100]).range([height, 100]);

  const lineColors = {
    0: foregroundColor,
    1: "#E9D758",
    2: "#48E5C2",
    3: "71A9F7",
  };

  var activateFunctions = [];
  var updateFunctions = [];

  function chart(selection) {
    selection.each(function (rawData) {
      svg = d3.select(this).selectAll("svg").data([adjustmentData]);
      var svgE = svg.enter().append("svg");

      svg = svg
        .merge(svgE)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

      g = svg
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

      var adjustmentData = getAdjustments(rawData);
      var keywordData = getKeywords(rawData);
      var tableData = getTableData(rawData);

      // Domain of X-axis can be set now, because the data has been loaded.
      var parseTime = d3.timeParse("%Y-%m-%d");
      var dates = [];

      for (let obj of adjustmentData) {
        dates.push(parseTime(obj.date));
      }

      xAdjustment.domain(d3.extent(dates));

      setupVis(adjustmentData, keywordData, tableData);

      setupSections();
    });
  }

  function setupVis(adjustmentData, keywordData, tableData) {
    function make_y_gridlines(yAdjustment) {
      return d3.axisLeft(yAdjustment).ticks(4).tickValues([25, 50, 75, 100]);
    }

    var parseTime = d3.timeParse("%Y-%m-%d");

    // X-axis.
    var axis = g
      .append("g")
      .attr("class", "x axis")
      .attr("transform", `translate(0, ${height})`)
      .attr("opacity", 1)
      .style("font-size", "12px")
      .style("font-family", "Roboto, sans-serif")
      .call(d3.axisBottom(xAdjustment));

    axis.selectAll("line").style("stroke", backgroundColor);

    axis.selectAll("path").style("stroke", backgroundColor);

    axis.selectAll("text").style("fill", backgroundColor);

    // Y-axis gridlines.
    g.append("g")
      .attr("class", "y gridlines")
      .attr("stroke-dasharray", "5, 5")
      .call(make_y_gridlines(yAdjustment).tickSize(-width).tickFormat(""))
      .call((g) => g.select(".domain").remove())
      .selectAll("line")
      .attr("opacity", 0.4)
      .style("stroke", backgroundColor);

    // Y-axis text.
    g.append("text")
      .attr("class", "y text")
      .attr("transform", "rotate(-90)")
      .attr("y", -40)
      .attr("x", -(height / 2) - 140)
      .attr("dy", "1em")
      .attr("opacity", 1)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "14px")
      .style("font-weight", "700")
      .style("letter-spacing", ".005em")
      .style("fill", backgroundColor)
      .text("AMOUNT OF SEARCHES →");

    // Title text.
    g.append("text")
      .attr("class", "title text")
      .attr("x", 158)
      .attr("y", 0 - margin.top / 2 + 80)
      .attr("opacity", 1)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "24px")
      .style("font-weight", "700")
      .style("fill", backgroundColor)
      .text("DATA");

    // Graph indicator.
    g.append("text")
      .attr("class", "title text2")
      .attr("x", 152)
      .attr("y", -(margin.top / 2) + 80)
      .attr("opacity", 1)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "24px")
      .style("font-weight", "700")
      .style("text-anchor", "end")
      .style("fill", foregroundColor)
      .text("");

    // Start line.
    g.append("g")
      .attr("class", "line start")
      .append("path")
      .datum(adjustmentData)
      .attr(
        "d",
        d3
          .line()
          .x(function (d) {
            return xAdjustment(+parseTime(d.date));
          })
          .y(function (d) {
            return yAdjustment(+d.start);
          })
      )
      .style("stroke", lineColors[0])
      .style("stroke-width", 1)
      .style("fill", "none");

    // Unadjusted line.
    g.append("g")
      .attr("class", "line unadjusted")
      .attr("opacity", 0)
      .append("path")
      .datum(adjustmentData)
      .attr(
        "d",
        d3
          .line()
          .x(function (d) {
            return xAdjustment(+parseTime(d.date));
          })
          .y(function (d) {
            return yAdjustment(+d.unadjusted);
          })
      )
      .style("stroke", lineColors[1])
      .style("stroke-width", 1)
      .style("fill", "none");

    // Adjusted line.
    g.append("g")
      .attr("class", "line adjusted")
      .attr("opacity", 0)
      .append("path")
      .datum(adjustmentData)
      .attr(
        "d",
        d3
          .line()
          .x(function (d) {
            return xAdjustment(+parseTime(d.date));
          })
          .y(function (d) {
            return yAdjustment(+d.normalised);
          })
      )
      .style("stroke", lineColors[2])
      .style("stroke-width", 1)
      .style("fill", "none");

    // Monthly line.
    g.append("g")
      .attr("class", "line monthly")
      .attr("opacity", 0)
      .append("path")
      .datum(adjustmentData)
      .attr(
        "d",
        d3
          .line()
          .x(function (d) {
            return xAdjustment(+parseTime(d.date));
          })
          .y(function (d) {
            return yAdjustment(+d.monthly);
          })
      )
      .style("stroke", lineColors[3])
      .style("stroke-width", 1)
      .style("fill", "none");

    // 6-month increments.
    g.append("g")
      .attr("class", "x gridlines")
      .attr("opacity", 0)
      .attr("transform", "translate(0," + height + ")")
      .call(
        d3
          .axisBottom(xAdjustment)
          .ticks(d3.timeMonth.every(6))
          .tickFormat("")
          .tickSize(-height + 100)
      )
      .selectAll("line")
      .attr("stroke", backgroundColor);

    // Columns.
    g.append("text")
      .attr("class", "table column date")
      .attr("x", 0)
      .attr("y", -(margin.top / 2) + 80)
      .attr("opacity", 0)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "18px")
      .style("font-weight", "700")
      .style("fill", backgroundColor)
      .text("Date");

    const tableLength = 20;

    for (var i = 0; i < tableLength; i++) {
      g.append("text")
        .attr("class", "table values date")
        .attr("x", 0)
        .attr("y", -(margin.top / 2) + 120 + i * 25)
        .attr("opacity", 0)
        .style("font-family", "Roboto, sans-serif")
        .style("font-size", "16px")
        .style("font-weight", "300")
        .style("fill", backgroundColor)
        .text(tableData[i].date);
    }

    g.append("text")
      .attr("class", "table column unadjusted")
      .attr("x", 150)
      .attr("y", -(margin.top / 2) + 80)
      .attr("opacity", 0)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "18px")
      .style("font-weight", "700")
      .style("fill", backgroundColor)
      .text("Unadjusted");

    for (var i = 0; i < tableLength; i++) {
      g.append("text")
        .attr("class", "table values unadjusted")
        .attr("x", 150)
        .attr("y", -(margin.top / 2) + 120 + i * 25)
        .attr("opacity", 0)
        .style("font-family", "Roboto, sans-serif")
        .style("font-size", "16px")
        .style("font-weight", "300")
        .style("fill", backgroundColor)
        .text(tableData[i].unadjusted);
    }

    g.append("text")
      .attr("class", "table column pct_change")
      .attr("x", 300)
      .attr("y", -(margin.top / 2) + 80)
      .attr("opacity", 0)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "18px")
      .style("font-weight", "700")
      .style("fill", backgroundColor)
      .text("Percentage Change");

    for (var i = 0; i < tableLength; i++) {
      g.append("text")
        .attr("class", `table values pct_change e${i}`)
        .attr("x", 300)
        .attr("y", -(margin.top / 2) + 120 + i * 25)
        .attr("opacity", 0)
        .style("font-family", "Roboto, sans-serif")
        .style("font-size", "16px")
        .style("font-weight", "300")
        .style("fill", backgroundColor)
        .text(tableData[i].pct_change);
    }

    g.append("text")
      .attr("class", "table column adjusted")
      .attr("x", 500)
      .attr("y", -(margin.top / 2) + 80)
      .attr("opacity", 0)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "18px")
      .style("font-weight", "700")
      .style("fill", backgroundColor)
      .text("Adjusted");

    for (var i = 0; i < tableLength; i++) {
      var j = i - 3;

      if (j < 0) {
        j += tableLength;
      }

      if (j == 17) {
        j = 19;
      } else if (j == 19) {
        j = 17;
      }

      g.append("text")
        .attr("class", `table values adjusted e${j}`)
        .attr("x", 500)
        .attr("y", -(margin.top / 2) + 120 + i * 25)
        .attr("opacity", 0)
        .style("font-family", "Roboto, sans-serif")
        .style("font-size", "16px")
        .style("font-weight", "300")
        .style("fill", backgroundColor)
        .text(tableData[i].adjusted);
    }

    g.append("text")
      .attr("class", "table column normalised")
      .attr("x", 650)
      .attr("y", -(margin.top / 2) + 80)
      .attr("opacity", 0)
      .style("font-family", "Roboto, sans-serif")
      .style("font-size", "18px")
      .style("font-weight", "700")
      .style("fill", backgroundColor)
      .text("Normalised");

    for (var i = 0; i < tableLength; i++) {
      g.append("text")
        .attr("class", "table values normalised")
        .attr("x", 650)
        .attr("y", -(margin.top / 2) + 120 + i * 25)
        .attr("opacity", 0)
        .style("font-family", "Roboto, sans-serif")
        .style("font-size", "16px")
        .style("font-weight", "300")
        .style("fill", backgroundColor)
        .text(tableData[i].normalised);
    }

    const allKeywords = [
      "debt",
      "color",
      "stocks",
      "restaurant",
      "portfolio",
      "inflation",
      "housing",
      "dow jones",
      "revenue",
      "economics",
      "credit",
      "markets",
      "return",
      "unemployment",
      "money",
      "religion",
      "cancer",
      "growth",
      "investment",
      "hedge",
      "marriage",
      "bonds",
      "derivatives",
      "headlines",
      "profit",
      "society",
      "leverage",
      "loss",
      "cash",
      "office",
      "fine",
      "stock market",
      "banking",
      "crisis",
      "happy",
      "car",
      "nasdaq",
      "gains",
      "finance",
      "sell",
      "invest",
      "fed",
      "house",
      "metals",
      "travel",
      "returns",
      "gain",
      "default",
      "present",
      "holiday",
      "water",
      "rich",
      "risk",
      "gold",
      "success",
      "oil",
      "war",
      "economy",
      "chance",
      "lifestyle",
      "greed",
      "food",
      "movie",
      "nyse",
      "ore",
      "opportunity",
      "health",
      "earnings",
      "arts",
      "culture",
      "bubble",
      "buy",
      "trader",
      "tourism",
      "politics",
      "energy",
      "consume",
      "consumption",
      "freedom",
      "dividend",
      "world",
      "conflict",
      "kitchen",
      "forex",
      "home",
      "cash",
      "transaction",
      "garden",
      "fond",
      "train",
      "labor",
      "fun",
      "environment",
      "ring",
    ];

    var selectedKeyword = "stock_market";

    autocomplete(document.getElementById("kwInput"), allKeywords);

    g.append("clipPath")
      .attr("id", "sliderClip")
      .append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", width)
      .attr("height", height);

    g.append("g")
      .attr("class", "line keyword")
      .attr("clip-path", "url(#sliderClip)")
      .attr("opacity", 0)
      .append("path")
      .datum(keywordData)
      .attr(
        "d",
        d3
          .line()
          .x(function (d) {
            return xAdjustment(+parseTime(d.date));
          })
          .y(function (d) {
            return yAdjustment(d[selectedKeyword]);
          })
      )
      .style("stroke", lineColors[3])
      .style("stroke-width", 1)
      .style("fill", "none");

    var dataTime = keywordData.map(function (obj) {
      return parseTime(obj.date);
    });

    var slider = d3
      .sliderBottom()
      .min(d3.min(dataTime))
      .max(d3.max(dataTime))
      .width(300)
      .tickFormat(d3.timeFormat("%Y"))
      .default([d3.min(dataTime), d3.max(dataTime)])
      .handle(d3.symbol().type(d3.symbolCircle).size(200)())
      .fill("#cccccc")
      .on("onchange", (date) => {
        xAdjustment.domain(date);

        g.selectAll(".x.axis").call(d3.axisBottom(xAdjustment));

        g.selectAll(".line.keyword path")
          .datum(keywordData)
          .attr(
            "d",
            d3
              .line()
              .x(function (d) {
                return xAdjustment(+parseTime(d.date));
              })
              .y(function (d) {
                return yAdjustment(d[selectedKeyword]);
              })
          );
      });

    function kwFunction() {
      selectedKeyword = $("#kwInput").val();

      g.selectAll(".line.keyword path")
        .datum(keywordData)
        .attr(
          "d",
          d3
            .line()
            .x(function (d) {
              return xAdjustment(+parseTime(d.date));
            })
            .y(function (d) {
              return yAdjustment(d[selectedKeyword.replace(" ", "_")]);
            })
        );

      g.selectAll(".title.text2")
        .transition()
        .duration(500)
        .text(`"${selectedKeyword}"`);
    }

    var gSlider = d3
      .selectAll("#dateSlider")
      .append("svg")
      .attr("width", 500)
      .attr("height", 100)
      .append("g")
      .attr("transform", "translate(30,30)");

    gSlider.call(slider);

    setupVis.kwFunction = kwFunction;
  }

  function setupSections() {
    activateFunctions[0] = emptyChart;
    activateFunctions[1] = unadjustedChart;
    activateFunctions[2] = incrementUnadjustedChart;
    activateFunctions[3] = unadjustedChart;
    activateFunctions[4] = percentageChangeTable;
    activateFunctions[5] = insertDataTable;
    activateFunctions[6] = inbetweenTable;
    activateFunctions[7] = adjustedChart;
    activateFunctions[8] = monthlyChart;
    activateFunctions[9] = exploreChart;

    for (var i = 0; i < activateFunctions.length; i++) {
      updateFunctions[i] = function () {};
    }
    updateFunctions[4] = updatePercentageChange;
    updateFunctions[5] = updateInsert;
  }

  // Activate functions.
  function emptyChart() {
    g.selectAll(".line.unadjusted")
      .transition()
      .duration(500)
      .attr("opacity", 0);

    g.selectAll(".title.text2")
      .transition()
      .duration(500)
      .style("fill", lineColors[0])
      .text("");

    g.selectAll(".y.text")
      .transition()
      .duration(500)
      .style("fill", backgroundColor);
  }

  function unadjustedChart() {
    g.selectAll(".table").transition().duration(500).attr("opacity", 0);

    g.selectAll(".line.adjusted").transition().duration(500).attr("opacity", 0);

    g.selectAll(".x.gridlines").transition().duration(500).attr("opacity", 0);

    g.selectAll(".y.gridlines").transition().duration(500).attr("opacity", 0.4);

    g.select(".x.axis").transition().duration(500).style("opacity", 1);

    g.selectAll(".line.unadjusted")
      .transition()
      .duration(500)
      .attr("opacity", 1);

    g.selectAll(".title.text2")
      .transition()
      .duration(500)
      .attr("opacity", 1)
      .style("fill", lineColors[1])
      .text("UNADJUSTED");

    g.selectAll(".y.text")
      .transition()
      .duration(500)
      .attr("opacity", 1)
      .style("fill", lineColors[1]);

    g.selectAll(".title.text").transition().duration(500).attr("opacity", 1);
  }

  function incrementUnadjustedChart() {
    g.selectAll(".y.gridlines").transition().duration(500).attr("opacity", 0);

    g.selectAll(".x.gridlines").transition().duration(500).attr("opacity", 0.4);
  }

  function percentageChangeTable() {
    g.selectAll(".x.axis").transition().duration(500).style("opacity", 0);

    g.selectAll(".y").transition().duration(500).attr("opacity", 0);

    g.selectAll(".title").transition().duration(500).attr("opacity", 0);

    g.selectAll(".line").transition().duration(500).attr("opacity", 0);

    g.selectAll(".table.column.adjusted")
      .transition()
      .duration(500)
      .attr("opacity", 0);

    g.selectAll(".table.values.adjusted")
      .transition()
      .duration(500)
      .attr("opacity", 0);

    g.selectAll(".table.column.date")
      .transition()
      .duration(500)
      .attr("opacity", 1);

    g.selectAll(".table.column.unadjusted")
      .transition()
      .duration(500)
      .attr("opacity", 1);

    g.selectAll(".table.column.pct_change")
      .transition()
      .duration(500)
      .attr("opacity", 1);

    g.selectAll(".table.values.date")
      .transition()
      .duration(500)
      .attr("opacity", 1);

    g.selectAll(".table.values.unadjusted")
      .transition()
      .duration(500)
      .attr("opacity", 1);
  }

  function insertDataTable() {
    g.selectAll(".table.column.normalised")
      .transition()
      .duration(500)
      .attr("opacity", 0);

    g.selectAll(".table.values.normalised")
      .transition()
      .duration(500)
      .attr("opacity", 0);

    g.selectAll(".table.values.pct_change").attr("opacity", 1);

    g.selectAll(".table.column.adjusted")
      .transition()
      .duration(500)
      .attr("opacity", 1);

    g.selectAll(".table.values.adjusted.e0").style("font-weight", 700);
  }

  function inbetweenTable() {
    g.selectAll(".x.axis").transition().duration(500).style("opacity", 0);

    g.selectAll(".y").transition().duration(500).attr("opacity", 0);

    g.selectAll(".title").transition().duration(500).attr("opacity", 0);

    g.selectAll(".line").transition().duration(500).attr("opacity", 0);

    g.selectAll(".table").transition().duration(500).attr("opacity", 1);

    g.selectAll(".table.values.adjusted.e0")
      .transition()
      .duration(500)
      .style("font-weight", 300);
  }

  function adjustedChart() {
    g.selectAll(".table").transition().duration(500).attr("opacity", 0);

    g.selectAll(".line.monthly").transition().duration(1000).attr("opacity", 0);

    g.selectAll(".x.axis").transition().duration(500).style("opacity", 1);

    g.selectAll(".title.text").transition().duration(500).attr("opacity", 1);

    g.selectAll(".y.gridlines").transition().duration(500).attr("opacity", 1);

    g.selectAll(".line.adjusted").transition().duration(500).attr("opacity", 1);

    g.selectAll(".title.text2")
      .transition()
      .duration(500)
      .attr("opacity", 1)
      .style("fill", lineColors[2])
      .text("ADJUSTED");

    g.selectAll(".y.text")
      .transition()
      .duration(500)
      .attr("opacity", 1)
      .style("fill", lineColors[2]);
  }

  function monthlyChart() {
    g.selectAll(".line.keyword").transition().duration(500).attr("opacity", 0);

    g.selectAll(".line.monthly").transition().duration(500).attr("opacity", 1);

    g.selectAll(".line.adjusted").transition().duration(500).attr("opacity", 1);

    g.selectAll(".title.text2").transition().duration(0).attr("opacity", 1);

    g.selectAll(".y.text").transition().duration(0).attr("opacity", 1);

    g.selectAll(".title.text2")
      .transition()
      .duration(500)
      .style("fill", lineColors[3])
      .text("MONTHLY");

    g.selectAll(".y.text")
      .transition()
      .duration(500)
      .style("fill", backgroundColor);
  }

  function exploreChart() {
    g.selectAll(".line.monthly").transition().duration(500).attr("opacity", 0);

    g.selectAll(".line.adjusted").transition().duration(500).attr("opacity", 0);

    g.selectAll(".line.keyword").transition().duration(500).attr("opacity", 1);
  }

  // Update functions.
  function updatePercentageChange(progress) {
    var progressInt = Math.floor(progress * 20) + 1;

    for (var i = 0; i < progressInt; i++) {
      g.selectAll(`.table.values.pct_change.e${i}`).attr("opacity", 1);
    }

    for (var i = 20; i > progressInt; i--) {
      g.selectAll(`.table.values.pct_change.e${i}`).attr("opacity", 0);
    }
  }

  function updateInsert(progress) {
    var progressInt = Math.floor(progress * 20) + 1;

    for (var i = 0; i < progressInt; i++) {
      g.selectAll(`.table.values.adjusted.e${i}`).attr("opacity", 1);
    }

    for (var i = 20; i > progressInt; i--) {
      g.selectAll(`.table.values.adjusted.e${i}`).attr("opacity", 0);
    }
  }

  // Data functions.
  function getAdjustments(rawData) {
    return rawData.map(function (obj) {
      return {
        date: obj.date,
        start: obj.start,
        unadjusted: obj.unadjusted,
        normalised: obj.normalised,
        monthly: obj.monthly,
      };
    });
  }

  function getTableData(rawData) {
    return rawData.map(function (obj) {
      return {
        date: obj.date,
        unadjusted: obj.unadjusted,
        pct_change: obj.pct_change,
        adjusted: obj.adjusted,
        normalised: obj.normalised,
      };
    });
  }

  function getKeywords(rawData) {
    return rawData.map(function (obj) {
      return {
        date: obj.date,
        debt: obj.debt,
        color: obj.color,
        stocks: obj.stocks,
        restaurant: obj.restaurant,
        portfolio: obj.portfolio,
        inflation: obj.inflation,
        housing: obj.housing,
        dow_jones: obj.dow_jones,
        revenue: obj.revenue,
        economics: obj.economics,
        credit: obj.credit,
        markets: obj.markets,
        return: obj.return,
        unemployment: obj.unemployment,
        money: obj.money,
        religion: obj.religion,
        cancer: obj.cancer,
        growth: obj.growth,
        investment: obj.investment,
        hedge: obj.hedge,
        marriage: obj.marriage,
        bonds: obj.bonds,
        derivatives: obj.derivatives,
        headlines: obj.headlines,
        profit: obj.profit,
        society: obj.society,
        leverage: obj.leverage,
        loss: obj.loss,
        cash: obj.cash,
        office: obj.office,
        fine: obj.fine,
        stock_market: obj.stock_market,
        banking: obj.banking,
        crisis: obj.crisis,
        happy: obj.happy,
        car: obj.car,
        nasdaq: obj.nasdaq,
        gains: obj.gains,
        finance: obj.finance,
        sell: obj.sell,
        invest: obj.invest,
        fed: obj.fed,
        house: obj.house,
        metals: obj.metals,
        travel: obj.travel,
        returns: obj.returns,
        gain: obj.gain,
        default: obj.default,
        present: obj.present,
        holiday: obj.holiday,
        water: obj.water,
        rich: obj.rich,
        risk: obj.risk,
        gold: obj.gold,
        success: obj.success,
        oil: obj.oil,
        war: obj.war,
        economy: obj.economy,
        chance: obj.chance,
        lifestyle: obj.lifestyle,
        greed: obj.greed,
        food: obj.food,
        movie: obj.movie,
        nyse: obj.nyse,
        ore: obj.ore,
        opportunity: obj.opportunity,
        health: obj.health,
        earnings: obj.earnings,
        arts: obj.arts,
        culture: obj.culture,
        bubble: obj.bubble,
        buy: obj.buy,
        trader: obj.trader,
        tourism: obj.tourism,
        politics: obj.politics,
        energy: obj.energy,
        consume: obj.consume,
        consumption: obj.consumption,
        freedom: obj.freedom,
        dividend: obj.dividend,
        world: obj.world,
        conflict: obj.conflict,
        kitchen: obj.kitchen,
        forex: obj.forex,
        home: obj.home,
        transaction: obj.transaction,
        garden: obj.garden,
        fond: obj.fond,
        train: obj.train,
        labor: obj.labor,
        fun: obj.fun,
        environment: obj.environment,
        ring: obj.ring,
      };
    });
  }

  // Activate.
  chart.activate = function (index) {
    activeIndex = index;

    var sign = activeIndex - lastIndex < 0 ? -1 : 1;
    var scrolledSections = d3.range(lastIndex + sign, activeIndex + sign, sign);

    scrolledSections.forEach(function (i) {
      activateFunctions[i]();
    });

    lastIndex = activeIndex;
  };

  chart.update = function (index, progress) {
    updateFunctions[index](progress);
  };

  scrollVis.setupVis = setupVis;

  return chart;
}

function display(data) {
  var plot = scrollVis();

  d3.select("#vis").datum(data).call(plot);

  var scroll = scroller().container(d3.select("#graphic"));

  scroll(d3.selectAll(".step"));

  scroll.on("active", function (index) {
    d3.selectAll(".step").style("opacity", function (d, i) {
      return i === index ? 1 : 0.1;
    });

    plot.activate(index);
  });

  scroll.on("progress", function (index, progress) {
    plot.update(index, progress);
  });
}

d3.csv("data/data.csv", display);
