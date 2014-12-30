var TableFilter = (function () {
    module = {}
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

    //Case insensitve contains selector
    jQuery.expr[':'].Contains = function (a, i, m) {
        return jQuery(a).text().toUpperCase()
            .indexOf(m[3].toUpperCase()) >= 0;
    };

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
        else if (typeof event != 'string' && !(event instanceof String))
            event.Event(inputId);
            event = event.name;


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

    function DefaultHandler(query)
    {
        return function (index, element){
            if($(element).text().toUpperCase().indexOf(query.toUpperCase()) != -1)
                return true
            return false
        }
    }


    module.SetupHandled = function (inputId, tableBodyId, handler, event){
        if (event == null)
            event = "keyup";
        else if (typeof event != 'string' && !(event instanceof String))
            event.Event(inputId);
            event = event.name;

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
    return module;
}());

