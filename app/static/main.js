// Get the modal
var textModal = document.getElementById("textModal");

// Get the button that opens the modal
var textBtn = document.getElementById("textBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close1")[0];

// When the user clicks on the button, open the modal
textBtn.onclick = function() {
  textModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  textModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    textModal.style.display = "none";
  }
}

// Get the modal
var emailModal = document.getElementById("emailModal");

// Get the button that opens the modal
var emailBtn = document.getElementById("emailBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close2")[0];

// When the user clicks on the button, open the modal
emailBtn.onclick = function() {
  emailModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  emailModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    emailModal.style.display = "none";
  }
}

