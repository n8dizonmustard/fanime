const options = {
    edge: 'left',
    draggable: 'true',
    inDuration: 250,
    outDuration: 200,
    onOpenStart: null,
    onOpenEnd: null,
    onCloseStart: null,
    onCloseEnd: null,
    preventScrolling: true,
    closeOnClick: false,
    numVisible: 5,
    dist: -100,
    autoPlay: true,
    autoStart: true,
    indicators: true
  }



 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, options);
  });