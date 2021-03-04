  
//   // When the user scrolls the page, execute myFunction
  window.onscroll = function() {sticky_navbar();};
  

  
  // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
  function sticky_navbar() {
    // Get the navbar
    var navbar = document.getElementById("myTopnav");
        
    // Get the offset position of the navbar
    var sticky = navbar.offsetTop;      
    if (window.pageYOffset > sticky) {
      navbar.classList.add("sticky")
    } else {
      navbar.classList.remove("sticky");
    }
  }