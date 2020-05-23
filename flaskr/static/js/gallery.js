$(function () {
  var $header = $('#header');
  var $frame = $('#frame');
  var $slider = $('#slider');
  var $themes = $('#themes');
  var $nav = $('#nav');
  var $image = $frame.find('.photo');
  var $caption = $frame.children('.photo-caption');
  var $thumbnails = $slider.children('#thumbnails');
  var $slider_btn = $slider.children('span');
  var thumbnails_width = 0;
  var $edge;
  var $selected;
  var currPhoto = 1;
  $(function () {
    firstThumbnail = $thumbnails.children(':first');
    selectThumbnail(firstThumbnail);
    thumb = thumbnails.querySelector('[data-index=\'' + currPhoto + '\']');
    $image.attr('src', thumb.dataset.fullimg);
    var first = firstThumbnail.children('img');
    if (first[0].complete) {
      initSlider()
    } else {
      first.load(initSlider)
    }
    $('body').css('opacity', '1')
  });
  $thumbnails.on('click', 'img', function (event) {
    $this = $(this);
    var photoID = parseInt($this.data('index'), 10);
    setImage(photoID);
    selectThumbnail($this.parent('li'), photoID);
    currPhoto = photoID
  });
  $frame.on('click', function (event) {
    if (currPhoto < $('[data-index]').length) {
      currPhoto++;
      nextThumbnail();
      $slider.find('.next').trigger('click')
    }
    setImage(currPhoto)
  });
  $nav.on('click', 'button', function (event) {
    var dir = this.className;
    if (dir.indexOf('prev') >= 0 && currPhoto > 1) {
      currPhoto--;
      prevThumbnail()
    } else if (dir.indexOf('next') >= 0 && currPhoto < $('[data-index]').length) {
      currPhoto++;
      nextThumbnail()
      $slider.find('.next').trigger('click')
    }
    setImage(currPhoto)
  });
  $(window).on('resize', function () {
    sliderDisplay();
    $thumbnails.children().css('display', 'inline-block');
    $edge = $thumbnails.children(':first');
    displaySliderBtn('prev', !1);
    displaySliderBtn('next', !0)
  });
  $slider.on('click', 'span', function (event) {
    var dir = event.target.className;
    var $first = $thumbnails.children(':first');
    var last_pos = getLastPos();
    if (dir.indexOf('prev') >= 0 && $first.css('display') == 'none') {
      $prev = $edge.prev();
      if ($prev.length > 0) {
        $edge = $prev
      }
      $edge.css('display', 'inline-block');
      if ($first[0] === $edge[0]) {
        displaySliderBtn('prev', !1)
      }
      displaySliderBtn('next', !0)
    } else if (dir.indexOf('next') >= 0 && last_pos > 0) {
      $edge.css('display', 'none');
      $edge = $edge.next();
      displaySliderBtn('prev', !0);
      if (getLastPos() === 0) {
        displaySliderBtn('next', !1)
      }
    }
  });
  $themes.on('click', 'span', function (event) {
    $this = $(this);
    theme = $this.data('theme');
    if (!$this.hasClass('active')) {
      if (theme == 'another') {
        $('link[href="/static/css/original.min.css"]').attr({
          href: '/static/css/another.min.css'
        });
        $nav.appendTo('#frame');
        $caption.appendTo('.photo-wrapper')
      } else {
        $('link[href="/static/css/another.min.css"]').attr({
          href: '/static/css/original.min.css'
        });
        $nav.appendTo('#header');
        $caption.appendTo('#frame')
      }
      $themes.children('.active').removeClass('active');
      $this.addClass('active')
    }
  });
  function setImage(photoID) {
    thumb = thumbnails.querySelector('[data-index=\'' + photoID + '\']');
    $image.attr('src', '');
    $image.attr('src', thumb.dataset.fullimg)
  }
  function selectThumbnail(thumbnail) {
    if ($selected) {
      $selected.removeClass('selected')
    }
    $selected = $(thumbnail);
    $selected.addClass('selected')
  }
  function prevThumbnail() {
    $selected.removeClass('selected');
    $selected = $selected.prev();
    $selected.addClass('selected')
  }
  function nextThumbnail() {
    $selected.removeClass('selected');
    $selected = $selected.next();
    $selected.addClass('selected')
  }
  function initSlider() {
    $thumbnails.children().each(function () {
      thumbnails_width += $(this).outerWidth(!0)
    });
    $edge = $thumbnails.children(':first');
    sliderDisplay();
    displaySliderBtn('prev', !1)
  }
  function sliderDisplay() {
    slider_width = $slider.innerWidth();
    if (slider_width < thumbnails_width && $slider_btn.css('display') == 'none') {
      $slider_btn.css('display', 'block')
    } else if (slider_width >= thumbnails_width && $slider_btn.css('display') == 'block') {
      $slider_btn.css('display', 'none')
    }
  }
  function displaySliderBtn(dir, display) {
    $btn = $slider.children('.' + dir);
    if (display) {
      $btn.removeClass('disable')
    } else {
      $btn.addClass('disable')
    }
  }
  function getLastPos() {
    var $last = $thumbnails.children(':last');
    return $last.position().top
  }
})

