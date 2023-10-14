document.addEventListener("DOMContentLoaded", function () {           
    const contactButton = document.getElementById("contact-button");           
    const topicsButton = document.getElementById("topics-button");    
    const aboutButton = document.getElementById("about-button");           
    const faqButton = document.getElementById("faq-button");           
    const resourcesButton = document.getElementById("get-started-button"); 
    const menuButton = document.getElementById("menu-button");
    const menuOverlay = document.getElementById("menu-overlay");
    const closeMenuLink = document.getElementById("close-menu");

        // Event listener for the "Menu" button click
        menuButton.addEventListener("click", function () {
            // Toggle the active class to show/hide the overlay
            menuOverlay.classList.toggle("active");
        });   
        
        closeMenuLink.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent the default link behavior (navigating)
            // Close the menu by removing the active class
            menuOverlay.classList.remove("active");
          });
    
 
    contactButton.addEventListener("click", function () {
        window.location.href = "contact.html";
    });          

    topicsButton.addEventListener("click", function () {
        window.location.href = "topics.html";
    });

    aboutButton.addEventListener("click", function () {
        window.location.href = "about.html";
    });          

    faqButton.addEventListener("click", function () {
        window.location.href = "FAQ.html";
    });

    resourcesButton.addEventListener("click", function () {
        window.location.href = "Resources.html";
    });

   
});