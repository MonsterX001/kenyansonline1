document.querySelectorAll("#").forEach(anchor => {
    anchor.addEventListener("click", function(e){
      e.preventDefault();
      document.querySelector(this.getAtribute("href")).ScrollIntoView({
        behaviour : "smooth"
      })
    })
  })
  
