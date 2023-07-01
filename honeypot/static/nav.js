const btn = document.getElementById("linkbtn");

// function for web share api
function webShareAPI(header, description, link) {
  navigator
    .share({
      title: header,
      text: description,
      url: link,
    })
    .then(() => console.log("Successful share"))
    .catch((error) => console.log("Error sharing", error));
}

if (navigator.share) {
  // Show button if it supports webShareAPI
  btn.style.display = "block";
  btn.addEventListener("click", () =>
    webShareAPI("Kenyans Online", "Upload videos and earn money, Talanta hella", "kenyansonline.com")
  );
} else {
  // Hide button if it doesn't supports webShareAPI
  btn.style.display = "none";
  console.error("Your Browser doesn't support Web Share API");
}





  /*let shareData = {
    title: 'MDN',
    text: 'Learn web development on MDN!',
    url: 'https://developer.mozilla.org',
  }

  const btns = document.querySelector('button');
  const resultPara = document.querySelector('.result');

  btns.addEventListener('click', () => {
    navigator.share(shareData)
      .then(() =>
        resultPara.textContent = 'MDN shared successfully'
      )
      .catch((e) =>
        resultPara.textContent = 'Error: ' + e
      )
  });*/
