﻿var TableFilter = (function () {
    module = {}
    //events
    module.Events = {}
    module.Events.doneTyping = (function () {
        var typingTimer;
        var doneTypingInterval = 300;
        instance = { 'name': 'doneTyping' }
        instance.Event = function (id) {
            id = "#" + id
            function DoneTypingHandler() {
                $(id).trigger(instance.name)
            }

            $(id).keyup(function () {
                clearTimeout(typingTimer);
                typingTimer = setTimeout(DoneTypingHandler, doneTypingInterval);
            });

            $(id).keydown(function () {
                clearTimeout(typingTimer);
            });
        }
        return instance;
    }());

    /* member methods */


    /*
 * Makes a table filterable based on an input field
 * inputId - The css id of the input field used to filter the table.
 * tableBodyId - The css id of the tbody tag we are filtering.
 * columns - An array of numbers that represent which columns should be considered when filtering. Can be null.
 * event - The event that should fire the filter functionality (keyup, change, etc.).
*/
    module.SetupIndexed = function (inputId, tableBodyId, columns, event) {
        if (event == null)
            event = "keyup";
        else if (typeof event != 'string' && !(event instanceof String)) {
            event.Event(inputId);
            event = event.name;
        }



        $("#" + inputId).on(event, function () {
            var rows = $("#" + tableBodyId).find("tr").hide();
            if (columns != null) {
                rows = $(rows).find(BuildIndexedQuery(columns));
                rows.filter(":Contains('" + this.value + "')").parent().show().css('display', "")
            }
            else {
                rows.filter(":Contains('" + this.value + "')").show().css('display', "");
            }
        });

    }

    //whenever the event is fired an ajax request is made to url. The url should have a parameter of 'query' which is the element at inputId's value.
    module.SetupAjaxed = function (inputId, tableBodyId, url, event) {
        if (event == null)
            event = "keyup";
        else if (typeof event != 'string' && !(event instanceof String)) {
            event.Event(inputId);
            event = event.name;
        }

        $("#" + inputId).on(event, function () {
            AjaxHandle(this.value, url, tableBodyId);
        })

    }

    //Allows execution of a handler function to determine if row shoud be included.
    module.SetupHandled = function (inputId, tableBodyId, handler, event) {
        if (event == null)
            event = "keyup";
        else if (typeof event != 'string' && !(event instanceof String)) {
            event.Event(inputId);
            event = event.name;
        }

        $("#" + inputId).on(event, function () {
            var rows = $("#" + tableBodyId).find("tr").hide();
            if (handler != null) {
                rows.filter(handler(this.value)).show().css('display', "")
            }
            else {
                rows.filter(DefaultHandler(this.value)).show().css('display', "");
            }
        });


    }

    /* Private Variables */
    var last_request;

    //Case insensitve contains selector
    jQuery.expr[':'].Contains = function (a, i, m) {
        return jQuery(a).text().toUpperCase()
            .indexOf(m[3].toUpperCase()) >= 0;
    };

    /* Private Functions */

    /*
     * Builds a string to be used as a selector to specify selecting specific columns in a row.
     * columns - An array of numbers that represent which columns should be included.
    */
    function BuildIndexedQuery(columns) {
        var query = ""
        for (var i = 0; i < columns.length; i++) {
            query += ":nth-child(" + columns[i] + ")";
            if (i < columns.length - 1) {
                query += ",";
            }
        }
        return query;
    }

    function AjaxHandle(query, url, tableBodyId) {
        if (last_request) {
            last_request.abort();
            last_request = null;
            console.log("request cancelled");
        }
        console.log("new request");
        last_request = $.ajax({
            url: url,
            type: "GET",
            data: { query: query },
            dataType: "html",
            success: function (data) {
                $("#" + tableBodyId).replaceWith(data);
                last_request = null;
            }
        });
    }

    function DefaultHandler(query) {
        return function (index, element) {
            if ($(element).text().toUpperCase().indexOf(query.toUpperCase()) != -1)
                return true
            return false
        }
    }

    return module;
}());