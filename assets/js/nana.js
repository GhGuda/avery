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








// Static exchange rate for Ghana
const ghanaDollarRate = 8;

// Function to calculate payout amount based on gift card amount and exchange rate
function calculatePayoutAmount() {
    // Get the gift card amount entered by the user
    const giftCardAmount = parseInt(document.getElementById("giftCardAmount").value);

    // Check if the entered value is a valid number
    if (!isNaN(giftCardAmount)) {
        // Calculate the payout amount in Ghana Cedis based on the gift card amount and exchange rate
        let payoutAmount = giftCardAmount * ghanaDollarRate;

        // Check if the payout amount is a whole number
        if (payoutAmount % 1 === 0) {
            // If it's a whole number, display without decimal places
            document.getElementById("payoutDetails").value = " " + payoutAmount.toFixed(0);
        } else {
            // If it's not a whole number, display with 2 decimal places
            document.getElementById("payoutDetails").value = " " + payoutAmount.toFixed(2);
        }
    } else {
        // If the entered value is not a valid number, display "Ghs 0" in the input field
        document.getElementById("payoutDetails").value = "₵ 0";
    }
}

// Function to handle input event on gift card amount input field
function handleGiftCardAmountInput() {
    // Calculate the payout amount based on the entered gift card amount and exchange rate
    calculatePayoutAmount();
}

// Add event listener to gift card amount input field to automatically update payout amount
document.getElementById("giftCardAmount").addEventListener("input", handleGiftCardAmountInput);

// Initial calculation based on default gift card amount (if any)
handleGiftCardAmountInput();








// List of types of gift cards
const giftCardTypes = [
    "Amazon",
    "iTunes",
    "Google Play",
    "Visa",
    "Mastercard",
    "Starbucks",
    "Walmart",
    "Target",
    "Netflix",
    "PlayStation",
    "Xbox",
    "Nintendo eShop",
    "Enter a gift card type", // Option for user to enter a custom gift card type
];

// Function to populate the select field with gift card types
function populateGiftCardTypes() {
    const giftCardTypeSelect = document.getElementById("giftCardType");

    // Loop through the gift card types array and create an option element for each type
    giftCardTypes.forEach((type) => {
        const option = document.createElement("option");
        option.value = type;
        option.textContent = type;
        giftCardTypeSelect.appendChild(option);
    });

    // Add event listener to the select field to show/hide other gift card type input
    giftCardTypeSelect.addEventListener("change", function() {
        const selectedOption = this.value;
        if (selectedOption === "Enter a gift card type") {
            document.getElementById("otherGiftCardTypeInput").style.display = "block";
        } else {
            document.getElementById("otherGiftCardTypeInput").style.display = "none";
        }
    });
}

// Call the function to populate the select field with gift card types
populateGiftCardTypes();
