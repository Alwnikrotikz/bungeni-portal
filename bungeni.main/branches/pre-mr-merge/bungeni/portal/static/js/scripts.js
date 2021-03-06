function listTogglr(){
  var viewletDateToggle = $('#whats-on-overview .whats-on-viewlet dd ul li h2');
  viewletDateToggle.css({
    background: 'url(/static/images/minus.png) 2px 4px no-repeat',
        paddingLeft: '20px',
        cursor: 'pointer'
        });
  viewletDateToggle.click(function(){
      var state = $(this).siblings('ul').css('display');
      if (state == 'hidden' || state == 'none') {
        $(this).css('background-image', 'url(/static/images/minus.png)');
        $(this).siblings('ul').slideDown('fast');
      }
      else {
        $(this).css('background-image', 'url(/static/images/plus.png)');
        $(this).siblings('ul').slideUp('fast');
      }
    });
  
  var viewlet = $('#fieldset-upcoming-sittings ul li ul li');
  // check if the link was clicked - if it was don't animate, just follow the link.
  var viewletLink = viewlet.children('a');
  var linkClicked = false;
  viewletLink.click(function(){
      linkClicked = true;
    });
  viewlet.css({
    background: '#fff url(/static/images/plus.png) 2px 4px no-repeat',
        paddingLeft: '20px',
        cursor: 'pointer'
        });
  $('#fieldset-upcoming-sittings ul li ul li ul li').css({background: '#fff', padding: '0'});
  viewlet.children('ul').hide();
  viewlet.click(function(){
      if(!linkClicked){
        var state = $(this).children('ul').css('display');
        if(state == 'hidden' || state == 'none'){
          $(this).css('background-image','url(/static/images/minus.png)');
          $(this).children('ul').slideDown('fast');
        }
        else {
          $(this).css('background-image','url(/static/images/plus.png)');
          $(this).children('ul').slideUp('fast');
        }
      }
    });
  $('#fieldset-upcoming-sittings ul li ul li ul li').css('cursor','default');
  $('#fieldset-upcoming-sittings ul li ul li ul li').click(function(){
      $(this).css('background','#fff');
    });
}
function searchTogglr(){
  var portletHeader = $('#portletArchiveDates .portletHeader');
  var portletHeaderSpan = portletHeader.children('span.tile');
  portletHeaderSpan.css({
      float:'right',
        display:'block',
        paddingLeft: '20px',
        cursor: 'pointer',
        background: 'url(/static/images/minus.png) 2px 4px no-repeat'
        });
  portletHeaderSpan.hover(function(){
      portletHeaderSpan.css('text-decoration','underline');
    },function(){
      portletHeaderSpan.css('text-decoration','none');
    });
  var portletItem = $('#portletArchiveDates .portletItem');
  portletItem.css({
    clear: 'both',
        height: '50px'
        });
  var portletItemForm = $('#portletArchiveDates .portletItem form');
  portletItemForm.css({
    display: 'block',
        position: 'absolute',
        top: 0,
        right: 0
        });
  
  if(!portletItem.hasClass('dates-filtered')){
    portletItem.hide();
    portletHeaderSpan.css('background-image','url(/static/images/plus.png)');
  }
  
  portletHeader.click(function(){
      var state = portletItem.css('display');
      if(state == 'hidden' || state == 'none'){
        portletHeaderSpan.css('background-image','url(/static/images/minus.png)');
        portletItem.slideDown('fast');
      }
      else {
        portletHeaderSpan.css('background-image','url(/static/images/plus.png)');
        portletItem.slideUp('fast');
      }
    });
}
$(document).ready(function(){
    searchTogglr();
    listTogglr();
    // Hides the dead links in the global nav.
    $('#portal-globalnav ul.level0 li a').each(function(){
        var link = $(this).attr('href');
        if(link.indexOf('#') != -1){
          $(this).parent().hide();
        }
      });
