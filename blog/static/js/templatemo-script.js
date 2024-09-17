icon =  document.querySelector(".nav-icon-btn")
$(function() {
    $(".navbar-toggler-main").on("click", function(e) {
        $(".tm-header").toggleClass("show");
        icon.classList.toggle("fa-times");
        e.stopPropagation();
      });

      $("html").click(function(e) {
        var header = document.getElementById("tm-header");

        if (!header.contains(e.target)) {
          icon.classList.remove("fa-times");
          $(".tm-header").removeClass("show");
        }
      });

      $("#tm-nav .nav-link").click(function(e) {
      icon.classList.remove("fa-times");
        $(".tm-header").removeClass("show");
      });
});

