console.log("Home page")

MicroModal.init({
  openTrigger: 'modal-open', // [3]
  closeTrigger: 'modal-close', // [4]
  openClass: 'is-open', // [5]
  disableScroll: true, // [6]
  disableFocus: false, // [7]
  awaitOpenAnimation: false, // [8]
  awaitCloseAnimation: false, // [9]
});
