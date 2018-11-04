d3.select("center").append("h3").text("HW4 Q3: Graph Visualization")

var width = 1200, height = 600;

var svg = d3.select("center").append("svg")
    .attr("width", width)
    .attr("height", height);

var g = svg.append("g").attr("transform", "translate(" + 
                                          width / 2 + 
                                          "," + 
                                          height / 2 + 
                                          ")");

var radiusScale = d3.scaleLinear()
    .domain([0, 2])
    .range([5, 30])

d3.csv("node.csv", function (node_data) {
  d3.csv("edge.csv", function (edge_data) {
    const nodes = node_data;
    console.log(node_data)
    const links = edge_data.map(function (a) {
      return {source: Number(a.source), target: Number(a.target)}
    });

    var simulation = d3.forceSimulation(nodes)
        .force("charge", d3.forceManyBody().strength(-500))
        .force("link", d3.forceLink(links).id(function (d) { return d.ID; }))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .on("tick", tick);

    var lineG = g.append("g")
        .attr("stroke", "#000")
        .attr("stroke-width", 1.5)
        .selectAll("line")
        .data(links)
        .enter()
        .append("line");

    var nodeG = g.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .enter()
        .append("circle");

    function tick() {
      lineG.attr("x1", function (d) { return d.source.x; })
           .attr("y1", function (d) { return d.source.y; })
           .attr("x2", function (d) { return d.target.x; })
           .attr("y2", function (d) { return d.target.y; });

      nodeG.attr("cx", function (d) { return d.x; })
           .attr("cy", function (d) { return d.y; })
           .attr("r", function (d) { return radiusScale(+d.PageRank); });
    }

    var colorScale = d3.scaleOrdinal(d3.schemeCategory20);
    // Highlight different componets
    // nodeG.style("fill", function (d) {
    //   return colorScale(d.Component)
    // });

    // Highlight PageRank
    nodeG.style("fill", function (d) {
      return "rgb(" + ((6 - d.PageRank) * 256 / 6) + ", " + ((6 - d.PageRank) * 256 / 6) + ", 255)";
    });

  })
})
