export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@6")
)});
  main.variable(observer()).define(["md"], function(md){return(
md`# Homework 4: Tree Explorer

This is Assignment 4 of IS545 for Spring 2021.
`
)});
  main.variable(observer("trees")).define("trees", ["d3"], function(d3){return(
d3.csv("https://gis-cityofchampaign.opendata.arcgis.com/datasets/979bbeefffea408e8f1cb7a397196c64_22.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D", d3.autoType)
)});
  main.variable(observer("signs")).define("signs", ["d3"], function(d3){return(
d3.csv("https://opendata.arcgis.com/datasets/f5aaae43ed6642cc944117f4f4221adb_37.csv", d3.autoType)
)});
  main.variable(observer("makeTrees")).define("makeTrees", ["d3","trees"], function(d3,trees){return(
function makeTrees() {
  const width = 450;
  const height = 450;
  const infoPanel = d3.select("#mytreeinfo");
  const svg = d3
  .create("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, 20, 20])
  .style("border", "solid 5px brown");
  // Note: aspect ratios!
  const xScale = d3.scaleLinear().domain(d3.extent(trees, d => d.X)).range([0.0, 20.0]);
  const yScale = d3.scaleLinear().domain(d3.extent(trees, d => d.Y)).range([20.0, 0.0]);
  svg.append("g")
    .attr("id", "trees")
    .selectAll("circle")
    .data(trees)
    .enter()
    .append("circle")
    .attr("cx", d => xScale(d.X))
    .attr("cy", d => yScale(d.Y))
    .attr("r", 0.02)
   // .style("fill", "green")
  .on("click", (e, d) => {
    infoPanel.text(`Location: ${d.ADDRESS} ${d.STREET} || Tree Family: ${d.FAMILY} || Condition: ${d.COND}`)
  })
  return {svg: svg, xScale: xScale, yScale: yScale};
}
)});
  main.variable(observer("makeSigns")).define("makeSigns", ["d3","signs"], function(d3,signs){return(
function makeSigns() {
  const width = 450;
  const height = 450;
  const infoPanel = d3.select("#mysigninfo");
  const svg = d3
  .create("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, 20, 20])
  .style("border", "solid 5px purple");
  // Note: aspect ratios! 
  const xScale = d3.scaleLinear().domain(d3.extent(signs, d => d.X)).range([0.0, 20.0]);
  const yScale = d3.scaleLinear().domain(d3.extent(signs, d => d.Y)).range([20.0, 0.0]);
  svg.append("g")
    .attr("id", "signs")
    .selectAll("circle")
    .data(signs)
    .enter()
    .append("circle")
    .attr("cx", d => xScale(d.X))
    .attr("cy", d => yScale(d.Y))
    .attr("r", 0.02)
  .on("click", (e, d) => {
    infoPanel.text(`Sign: ${d.Sign_Type} || Category: ${d.Category}`)
  })
  return {svg: svg, xScale: xScale, yScale: yScale};
}
)});
  main.variable(observer()).define(["md"], function(md){return(
md`# Trees

Here you can see which Tree you have clicked on. The first map can be panned and zoomed around. The second map will allow you to brush and select multiple clusters of trees in a rectangular area.
`
)});
  main.variable(observer()).define(["html"], function(html){return(
html`<div id = "mytreeinfo"></div>`
)});
  main.variable(observer()).define(["makeTrees","d3"], function*(makeTrees,d3)
{
  const {svg, xScale, yScale} = makeTrees();
  yield svg.node();
  const zoom = d3.zoom();
  function zoomCalled(event){
    const zx = event.transform.rescaleX(xScale);
    const zy = event.transform.rescaleY(yScale);
    svg.select("g#trees").attr("transform", event.transform);
  }
  svg.call(zoom.on("zoom", zoomCalled));
}
);
  main.variable(observer()).define(["makeTrees","d3","trees"], function*(makeTrees,d3,trees)
{
  const {svg, xScale, yScale} = makeTrees();
  yield svg.node();
  const treeGroup = svg.select("g#trees");
  const brush = d3.brush().extent([[0, 0], [20, 20]]).handleSize(0.1);
  function brushCalled(event) {
    treeGroup.selectAll("circle")
    .data(trees)
    .classed("selected", d => xScale(d.X) > event.selection[0][0]
                && xScale(d.X) < event.selection[1][0]
                && yScale(d.Y) > event.selection[0][1]
                && yScale(d.Y) < event.selection[1][1] );
  }
  svg.append("g")
    .attr("class", "mybrush")
    .style("stroke-width", 0.01)
    .call(brush.on("brush", brushCalled));
}
);
  main.variable(observer()).define(["html"], function(html){return(
html`
<style>
  .selected { fill: orange; }
</style>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`# Traffic Signs

Here you can see which traffic sign you have clicked on. The first map can be panned and zoomed around. The second map will allow you to brush and select multiple clusters of traffic signs in a rectangular area.
`
)});
  main.variable(observer()).define(["html"], function(html){return(
html`<div id = "mysigninfo"></div>`
)});
  main.variable(observer()).define(["makeSigns","d3"], function*(makeSigns,d3)
{
  const {svg, xScale, yScale} = makeSigns();
  yield svg.node();
  const zoom = d3.zoom();
  function zoomCalled(event){
    const zx = event.transform.rescaleX(xScale);
    const zy = event.transform.rescaleY(yScale);
    svg.select("g#signs").attr("transform", event.transform);
  }
  svg.call(zoom.on("zoom", zoomCalled));
}
);
  main.variable(observer()).define(["makeSigns","d3","signs"], function*(makeSigns,d3,signs)
{
  const {svg, xScale, yScale} = makeSigns();
  yield svg.node();
  const signGroup = svg.select("g#signs");
  const brush = d3.brush().extent([[0, 0], [20, 20]]).handleSize(0.1);
  function brushCalled(event) {
    signGroup.selectAll("circle")
    .data(signs)
    .classed("selected", d => xScale(d.X) > event.selection[0][0]
                && xScale(d.X) < event.selection[1][0]
                && yScale(d.Y) > event.selection[0][1]
                && yScale(d.Y) < event.selection[1][1] );
  }
  svg.append("g")
    .attr("class", "mybrush")
    .style("stroke-width", 0.01)
    .call(brush.on("brush", brushCalled));
}
);
  main.variable(observer()).define(["html"], function(html){return(
html`
<style>
  .selected { fill: orange; }
</style>
`
)});
  return main;
}
