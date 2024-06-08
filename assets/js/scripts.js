document.addEventListener('DOMContentLoaded', function () {
    const lightIcon = document.getElementById('light-icon');
    const darkIcon = document.getElementById('dark-icon');
    const body = document.body;
  
    // Check for saved mode in local storage
    const savedMode = localStorage.getItem('mode');
  
    if (savedMode === 'dark-mode') {
      body.classList.add('dark-mode');
      // Show the moon icon when in dark mode
      darkIcon.style.display = 'inline';
      lightIcon.style.display = 'none';
    } else {
      // Show the lightbulb icon when in light mode
      lightIcon.style.display = 'inline';
      darkIcon.style.display = 'none';
    }
  
    // Toggle between dark and light mode
    lightIcon.addEventListener('click', toggleMode);
    darkIcon.addEventListener('click', toggleMode);
  
    function toggleMode() {
      body.classList.toggle('dark-mode');
      const newMode = body.classList.contains('dark-mode') ? 'dark-mode' : 'light-mode';
      localStorage.setItem('mode', newMode);
      // Toggle visibility of icons
      lightIcon.style.display = body.classList.contains('dark-mode') ? 'none' : 'inline';
      darkIcon.style.display = body.classList.contains('dark-mode') ? 'inline' : 'none';
    }
  });





  // Scroll section active links

// let sections = document.querySelectorAll('.top, .wedo');
// let navLinks = document.querySelectorAll('.navLinks ul li a');

// window.onscroll = () => {
//     sections.forEach(section => {
//         let top = window.scrollY;
//         let offset = section.offsetTop - 150;
//         let height = section.offsetHeight;
//         let id = section.getAttribute('id');

//         if (top >= offset && top < offset + height) {
//             navLinks.forEach(link => {
//                 link.classList.remove('active');
//             });
//             document.querySelector('.navLinks ul li a[href="#' + id + '"]').classList.add('active');
//         };
//     });
// };




const typed = new Typed('.multiple-text', {
  strings: ['Amazon', 'Starbucks', 'iTunes', 'Walmart', 'Target', 'Google Play', 'Google Play', 'Best Buy',
             'Home Depot', 'Sephora', 'Apple Store', 'Netflix', "Macy's", 'Xbox/PlayStation Store', 'Airbnb', 'And many more...'],
  typeSpeed: 100, // Adjust speed as needed
  loop: true
});



// BREAKPOINT TOGGLER 


var toggler = document.querySelector('.toggler');
var main = document.querySelector('.navLinks');
toggler.addEventListener('click', function() {
    main.classList.toggle('navLinks-active');
});


//Accordion


var dropButtons = document.querySelectorAll('.drop');

  dropButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      var lome = this.parentElement.nextElementSibling;
      if (lome.style.display === 'none' || lome.style.display === '') {
          lome.style.display = 'block';
          this.textContent = 'Close';
      } else {
          lome.style.display = 'none';
          this.textContent = 'Details';
      }
  });
});



// Get all currency buttons
var currencyButtons = document.querySelectorAll('.currency button');

// Loop through each currency button
currencyButtons.forEach(function(button) {
    // Add click event listener to each currency button
    button.addEventListener('click', function() {
        // Remove "active" class from all currency buttons
        currencyButtons.forEach(function(btn) {
            btn.classList.remove('active');
        });
        // Add "active" class to the clicked button
        this.classList.add('active');
    });
});



// Prevent page reload

function redirectWithoutLoad(event) {
  event.preventDefault(); // Prevent default anchor behavior (page load)
  var targetPage = event.currentTarget.getAttribute('href');
  window.location.href = targetPage;
}






// Function to slide cards automatically
document.addEventListener('DOMContentLoaded', function() {
  // Function to slide cards automatically
  function slideCards() {
      const cardContainer = document.getElementById('card-container');
      const firstCard = cardContainer.querySelector('.saycard');

      // Calculate width of a single card
      const cardWidth = firstCard.offsetWidth + parseInt(window.getComputedStyle(firstCard).marginRight);

      // Move the first card to the end
      cardContainer.appendChild(firstCard.cloneNode(true));
      cardContainer.removeChild(firstCard);

      // Reset scroll position to maintain view
      cardContainer.scrollLeft += cardWidth;
  }

  // Slide cards every 5 seconds (adjust as needed)
  setInterval(slideCards, 5000);
});