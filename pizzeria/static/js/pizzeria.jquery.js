String.prototype.toHHMMSS = function () {
    sec_numb = parseInt(this);
    var hours = Math.floor(sec_numb / 3600);
    var minutes = Math.floor((sec_numb - (hours * 3600)) / 60);
    var seconds = sec_numb - (hours * 3600) - (minutes * 60);

    if (hours < 10) {hours = "0" + hours;}
    if (minutes < 10) {minutes = "0" + minutes;}
    if (seconds < 10) {seconds = "0" + seconds;}

    var time = hours + ':' + minutes + ':' + seconds;
    return time;
};

(function($) {
    /**
     * Async-updates all rows in an html table with the status of an order,
     * retrieved via a server call.
     * Row IDs must be of the form: order-12
     * Time Elapsed and Order Complete <td> cells must have classes of
     * "elapsed" and "is_complete", respectively.
     */
    $.fn.pizzeriaOrderStatus = function() {
        var orderEls = this;

        // Put the IDs into an array of ints
        var orderIds = [];
        this.each(function() {
            var orderId = parseInt(this.id.slice(6));
            orderIds.push(orderId);
        });

        var doDataRefresh = function() {
            $.ajax({
                url: "/api/order-info/",
                data: {order_ids: orderIds.join(",")},
                dataType: "json",
                success: function(orders) {
                    $.each(orderEls, function() {
                        // Set data elements on nodes for each order.
                        $(this).find('.is_complete').data(
                            'time_complete', orders[this.id].time_closed);
                        // Only update seconds elapsed if not set yet, to avoid
                        // delays from network latency.  We manually increment this
                        // (below).
                        if (!$(this).find('.elapsed').data('seconds')) {
                            $(this).find('.elapsed').data(
                                'seconds', orders[this.id].seconds_elapsed);
                        }
                    });
                }
            });
        };

        // Query the server every 5 seconds to check order completion.
        doDataRefresh();
        setInterval(doDataRefresh, 5000);

        var doTableUpdate = function() {
            $.each(orderEls, function() {
                // Naively update time elapsed by a second or set completion
                // indicator.
                var el = $(this).find('.elapsed');
                var seconds = el.data('seconds');
                if (seconds >= 0) {
                    var time_closed = $(this).find('.is_complete');
                    if (time_closed.data('time_complete')) {
                        el.html(
                            '<span class="green">' + seconds.toString().toHHMMSS());
                        var time = time_closed.data('time_complete');
                        time_closed.html(
                                '<span class="green">' + time + '</span>');
                    }
                    else {
                        seconds += 1;
                        el.data('seconds', seconds)
                            .html('<span class="red">' + seconds.toString().toHHMMSS());
                        time_closed.html(
                            '<span class="red">No</span>');
                    }
                }

                // Update order completion status.
            });
        };

        // Update the display every second.
        doTableUpdate();
        setInterval(doTableUpdate, 1000);

        return this;
    };
})(jQuery);
