function dynamicChart(chart, parentElement) {
  function process_chart() {
    if ($(window).width() > 600) {
      chart.el.find("svg").css("height", `${$(parentElement).height()}px`);
    } else {
      // small devices
      chart.el.find("svg").css("height", "250px");
    }
    chart.redraw()
  }

  $(window).on("resize", function() {
    setTimeout(function(){
      process_chart();
    }, 280);
  });

  process_chart();
}
