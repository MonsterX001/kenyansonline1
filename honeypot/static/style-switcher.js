const styleSwitcherToggle = document.querySelector(".style-switcher-toggle");
styleSwitcherToggle.addEventListener("click", () => {
    document.querySelector(".style-switcher").classList.toggle("open");
})
window.addEventListener("scroll", () =>{
    if(document.querySelector(".style-switcher").classList.contains("open"))
    {
        document.querySelector(".style-switcher").classList.remove('open');
    }
})

const alternateStyles = document.querySelectorAll(".alternate-style");
function setActiveStyle(color)
{
    alternateStyles.forEach((style) => {
        if(color === style.getAttribute("title")){
            style.removeAttribute("disabled");
        }
        else{
            style.setAttribute("disabled", "True")
        }
    })
}

const dayNight = document.querySelector(".day-night");

dayNight.addEventListener("click", () => {
  dayNight.querySelector("i").classList.toggle("fa-solid fa-sun-bright");
  dayNight.querySelector("i").classList.toggle("fa-solid fa-moon");
  document.body.classList.toggle("dark");

  // Save the mode to local storage
  const isDarkMode = document.body.classList.contains("dark");
  localStorage.setItem("mode", isDarkMode ? "dark" : "light");
});

window.addEventListener("load", () => {
  // Retrieve the mode from local storage
  const savedMode = localStorage.getItem("mode");

  if (savedMode === "dark") {
    dayNight.querySelector("i").classList.add("fa-solid", "fa-sun-bright");
    document.body.classList.add("dark");
  } else {
    dayNight.querySelector("i").classList.add("fa-solid", "fa-moon");
    document.body.classList.remove("dark");
  }
});
