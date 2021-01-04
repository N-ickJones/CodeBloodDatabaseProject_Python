//Start Variables
let windowX = $(window).width(),
    windowY = $(window).height(),
    pageWidth = document.body.style.width,
    pageHeight = document.body.style.height;
let dropButtonToggle = false,
    loginButtonToggle = false;
//End Variables
//Initialize Screen
screenChange();
//End Initialize Screen
//Screen Resize
window.addEventListener("resize", screenChange);
  function screenChange () {
      windowX = $(window).width();
      windowY = $(window).height();
      pageWidth = windowX.toString() + "px";
      pageHeight = windowY.toString() + "px";
      //Fonts
    if(windowX <= 1040){
        document.getElementById('nav-menu').style.display = "none";
        document.getElementById('drop-down').style.display = "block";
        document.getElementById('drop-button').style.width = (windowX / 10) + "px";
        document.getElementById('drop-button').style.height = (windowX / 12) + "px";
        //document.getElementById('drop-menu').style.width = (windowX / 10 + 2) + "px";
        document.getElementById('drop-menu').style.display = "none";
    }
    else {
         document.getElementById('nav-menu').style.display = "flex";
         document.getElementById('drop-down').style.display = "none";
     }
  }
//End Screen Resize
function loginButtonClick() {

    if(!loginButtonToggle) {
        document.getElementById('top-menu-drop-box').style.display = "flex";
        loginButtonToggle = true;
    }
    else {
        document.getElementById('top-menu-drop-box').style.display = "none";
        loginButtonToggle = false;
    }
    }
  document.getElementById('drop-button').addEventListener('click', () => {

    if(!dropButtonToggle) {
        document.getElementById('drop-menu').style.display = "block";
        dropButtonToggle = true;
    }
    else{
        document.getElementById('drop-menu').style.display = "none";
        dropButtonToggle = false;
    }
  });
  document.getElementById('drop-label').addEventListener('click', () => {
    if(!dropButtonToggle) {
        document.getElementById('drop-menu').style.display = "block";
        dropButtonToggle = true;
    }
    else{
        document.getElementById('drop-menu').style.display = "none";
        dropButtonToggle = false;
    }
  });
  $(document).on("click", function (e) {

   if((e.target.className !== 'login-interface') && (loginButtonToggle = 'True')){
       $("#top-menu-drop-box").hide();
       loginButtonToggle = false;
   }});
   //if ((e.target.className !== 'drop-interface') && (dropButtonToggle = 'True')) {
   //     $("#drop-menu").hide();
   //
   //    dropButtonToggle = false;
   //}
  //});