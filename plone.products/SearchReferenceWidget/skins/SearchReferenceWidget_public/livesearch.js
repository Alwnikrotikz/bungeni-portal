var livesearch = function (){

    // Delay in milliseconds until the search starts after the last key was
    // pressed. This keeps the number of requests to the server low.
    var _search_delay = 400;
    // Delay in milliseconds until the results window closes after the
    // searchbox looses focus.
    var _hide_delay = 400;

    // stores information for each searchbox on the page
    var _search_handlers = {};

    // constants for better compression
    var _LSHighlight = "LSHighlight";
    var _cssQuery = cssQuery;
    var _registerEventListener = registerEventListener;
    var _removeClassName = removeClassName;
    var _addClassName = addClassName;

    function _isform($node) {
        // return true if the node is a form. used for findContainer in _setup.
        //DJJ: don't rely on single form
        if ($node.tagName && ($node.tagName == 'FORM' || $node.tagName == 'form') ||
            $node.className && ($node.className == 'LSBox')) {
            return true;
        }
        return false;
    };

    function _searchfactory($form, $inputnode) {
        // returns the search functions in a dictionary.
        // we need a factory to get a local scope for the event, this is
        // necessary, because IE doesn't have a way to get the target of
        // an event in a way we need it.
        var $lastsearch = null;
        var $request = null;
        var $cache = {};
        var $querytarget = _cssQuery("input.querytarget", $form);
        if ($querytarget.length == 1) {
        	$querytarget = $querytarget[0];
        } else {
        	$querytarget = null;
		}        
        var $min_chars = _cssQuery("input.min_chars", $form);
        if ($min_chars.length == 1) {
        	$min_chars = $min_chars[0];
        } else {
        	$min_chars = null;
		}        
        var $$result = _cssQuery("div.LSResult", $form);
        if ($$result.length != 1)
            return;
        $$result = $$result[0];
        var $shadow = _cssQuery("div.LSShadow", $form);
        if ($shadow.length != 1)
            return;
        $shadow = $shadow[0];
        var $path = _cssQuery("input[name=path]", $form);
        if ($path.length == 1) {
            $path = $path[0];
        } else {
            $path = null;
        }


        function _hide() {
            // hides the result window
            $$result.style.display = "none";
            $lastsearch = null;
        };

        function _hide_delayed() {
            // hides the result window after a showrt delay
            window.setTimeout("livesearch.hide('"+$form.id+"')", _hide_delay);
        };

        function _show($data) {
            // shows the result
            $$result.style.display = "block";
            $shadow.innerHTML = $data;
        };

        function _search() {
            // does the actual search
            if ($lastsearch == $inputnode.value) {
                // do nothing if the input didn't change
                return;
            }
            if ($request && $request.readyState < 4) {
                // abort any pending request
                $request.abort();
            }
            // Do nothing as long as we have less then two characters - 
            // the search results makes no sense, and it's harder on the server.
            var $min_chars_now = 2;
            if ($min_chars != null) {
            	$min_chars_now = parseInt($min_chars.value);
            }
            
            if ($inputnode.value.length < $min_chars_now) {
                _hide();
                return;
            }
            if ($querytarget != null) {
	            $base_query = $querytarget.value
	        } else {
	        	$base_query = "livesearch_reply?q=";
	        }
            
            if ($path && $path.checked) {
                $$current_path = $base_query + "&path=" + encodeURIComponent($path.value);
            } else {
                $$current_path = $base_query;
            }
            // check cache
            if ($cache[$$current_path]) {
                var $data = $cache[$$current_path][$inputnode.value];
                if ($data) {
                    _show($data);
                    return;
                }
            }
            // prepare the search request
            $request = new XMLHttpRequest();
            $request.onreadystatechange = function() {
                if ($request.readyState == 4) {
                    if ($request.status > 299 ||
                        $request.status < 200 ||
                        $request.responseText.length < 10) {
                        return;
                    }
                    // show results if there are any and cache them
                    _show($request.responseText);
                    if (!$cache[$$current_path]) {
                        $cache[$$current_path] = {};
                    }
                    $cache[$$current_path][$lastsearch] = $request.responseText;
                }
            };
	        if (typeof portal_url != "undefined") {
    	        $qurl = portal_url + "/";
        	}
            $request.open("GET", $qurl + $$current_path + encodeURIComponent($inputnode.value));
            $lastsearch = $inputnode.value;
            // start the actual request
            $request.send(null);
        };

        function _search_delayed() {
            // search after a small delay, used by onfocus
            window.setTimeout("livesearch.search('"+$form.id+"')", _search_delay);
        };

        return {
            hide: _hide,
            hide_delayed: _hide_delayed,
            search: _search,
            search_delayed: _search_delayed
        };
    };

    function _keyhandlerfactory($form) {
        // returns the key event handler functions in a dictionary.
        // we need a factory to get a local scope for the event, this is
        // necessary, because IE doesn't have a way to get the target of
        // an event in a way we need it.
        var $timeout = null;
        var $$result = _cssQuery("div.LSResult", $form);
        if ($$result.length != 1)
            return;
        $$result = $$result[0];
        var $shadow = _cssQuery("div.LSShadow", $form);
        if ($shadow.length != 1)
            return;
        $shadow = $shadow[0];

        function _keyUp($event) {
            // select the previous element
            var $listitems = _cssQuery("li", $shadow);
            var i;
            for (i=0; i<$listitems.length; i++) {
                if (hasClassName($listitems[i], _LSHighlight))
                    break;
            }
            if (i < $listitems.length) {
                _removeClassName($listitems[i], _LSHighlight);
                i--;
                if (i < 0)
                    i = $listitems.length - 1;
                _addClassName($listitems[i], _LSHighlight);
            } else {
                _addClassName($listitems[$listitems.length - 1], _LSHighlight);
            }
            if (typeof $event.preventDefault != "undefined")
                $event.preventDefault();
        };

        function _keyDown($event) {
            // select the next element
            var $listitems = _cssQuery("li", $shadow);
            var i;
            for (i=0; i<$listitems.length; i++) {
                if (hasClassName($listitems[i], _LSHighlight))
                    break;
            }
            if (i < $listitems.length) {
                _removeClassName($listitems[i], _LSHighlight);
                i++;
                if (i >= $listitems.length)
                    i = 0;
                _addClassName($listitems[i], _LSHighlight);
            } else {
                _addClassName($listitems[0], _LSHighlight);
            }
            if (typeof $event.preventDefault != "undefined")
                $event.preventDefault();
        };

        function _keyEscape($event) {
            // hide results window
            var $highlights = _cssQuery("li.LSHighlight", $shadow);
            for (var i=0; i<$highlights.length; i++) {
                _removeClassName($highlights[i], _LSHighlight);
            }
            $$result.style.display = "none";
        };

        function _handler($event) {
            // dispatch to specific functions and handle the search timer
            if (!$event) var $event = window.event;
            window.clearTimeout($timeout);
            switch ($event.keyCode) {
                case 38: _keyUp($event);
                    break;
                case 40: _keyDown($event);
                    break;
                case 27: _keyEscape($event);
                    break;
                case 37: break; // keyLeft
                case 39: break; // keyRight
                default: {
                    $timeout = window.setTimeout("livesearch.search('"+$form.id+"')", _search_delay);
                }
            }
        };

        function _submit($event) {
            // check whether a search result was selected with the keyboard
            // and open it
            if (!$event) var $event = window.event;
            var $targets = _cssQuery("li.LSHighlight a", $shadow);
            if ($targets.length > 0) {
                var $target = $targets[0].href;
                if (!$target)
                    return true;
                window.location = $target;
                return false;
            }
            return true;
        };

        return {
            handler: _handler,
            submit: _submit
        }
    };

    function _setup($inputnode, $number) {
        // set up all the event handlers and other stuff
        var $form = findContainer($inputnode, _isform);

        // add an id which is used by other functions to find the correct node
        $form.id = "livesearch"+$number;
        $form.style['white-space'] = 'nowrap';
        $inputnode.setAttribute("autocomplete","off");

        var $key_handler = _keyhandlerfactory($form);
        _search_handlers[$form.id] = _searchfactory($form, $inputnode);
        $form.onsubmit = $key_handler.submit;
        _registerEventListener($inputnode, "keydown", $key_handler.handler);
        _registerEventListener($inputnode, "focus", _search_handlers[$form.id].search_delayed);
        _registerEventListener($inputnode, "blur", _search_handlers[$form.id].hide_delayed);
    };

    function _init() {
        if (!W3CDOM)
            return; // the browser doesn't support enough functions
        // find all search fields and set them up
        var $gadgets = _cssQuery("input.portlet-search-gadget,#searchGadget");
        for (var i=0; i < $gadgets.length; i++) {
            _setup($gadgets[i], i);
        }
    };

    /*registerPloneFunction(_init);*/
    registerEventListener(window, "load", _init); /*DJJ: need to run after widgets loaded*/

    return {
        search: function(id) {
            _search_handlers[id].search();
        },
        hide: function(id) {
            _search_handlers[id].hide();
        }
    };
}();