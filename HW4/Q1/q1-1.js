d3.select("center").append("h3").text("HW4 Q1: Random data TSNE")


const width = 1000,
      height = 700,
      margin = 50,

      colorScale = d3.scaleOrdinal(d3.schemeCategory20),

      centerx = d3.scaleLinear()
          .range([width / 2 - height / 2 + margin,
                  width / 2 - height / 2 - margin]),
      centery = d3.scaleLinear()
          .range([margin, height - margin]);

function draw(canvas, nodes) {
  let context = canvas.node().getContext("2d");
  context.clearRect(0, 0, width, width);

  for (var i = 0, n = nodes.length; i < n; ++i) {
    var node = nodes[i];
    context.beginPath();
    context.moveTo(node.x, node.y);
    context.arc(node.x, node.y, 20, 0, 2 * Math.PI);

    context.lineWidth = 0.5;
    context.fillStyle = node.color;
    context.fill();

    context.fillStyle = "black";
    context.font = "20px Open Sans";
    context.fillText(node.text, node.x, node.y);
  }
}


d3.csv("random.csv", function (src_data) {
  const data = src_data.map((d, i) => Object.values(d));

  const canvas = d3.select("center").append("canvas")
      .attr("width", width)
      .attr("height", height);

  const model = new tsnejs.tSNE({
    dim: 2,
    perplexity: 30,
  });

  var features = data.map(function (value, index) {
    return value.slice(1, -1);
  });
  model.initDataRaw(features);

  const forcetsne = d3.forceSimulation(
    data.map(
      d => (d.x = width / 2, d.y = height / 2, d)
    )
  )
  .alphaDecay(0.005)
  .alpha(0.1);

  forcetsne.force("tsne", function (alpha) {
    model.step();
    let pos = model.getSolution();
    centerx.domain(d3.extent(pos.map(d => d[0])));
    centery.domain(d3.extent(pos.map(d => d[1])));
    data.forEach((d, i) => {
      d.x += alpha * (centerx(pos[i][0]) - d.x);
      d.y += alpha * (centery(pos[i][1]) - d.y);
    });
  })
  .force("collide", d3.forceCollide().radius(d => 10));

  forcetsne.on("tick", function () {
    let nodes = data.map((d, i) => {
      return {
        x: d.x,
        y: d.y,
        color: colorScale(d[d.length - 1]),
        text: d[0]
      };
    });

    draw(canvas, nodes);
  });

})
