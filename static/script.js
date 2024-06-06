$(document).ready(function() {
    $('#country').change(function() {
        let country = $(this).val();
        if (country) {
            $.ajax({
                url: '/states',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({country: country}),
                success: function(data) {
                    $('#state').empty().append('<option value="">Select State</option>');
                    $.each(data, function(index, value) {
                        $('#state').append('<option value="' + value + '">' + value + '</option>');
                    });
                    $('#state').prop('disabled', false);
                    $('#city').empty().append('<option value="">Select City</option>').prop('disabled', true);
                }
            });
        } else {
            $('#state').empty().append('<option value="">Select State</option>').prop('disabled', true);
            $('#city').empty().append('<option value="">Select City</option>').prop('disabled', true);
        }
    });

    $('#state').change(function() {
        let country = $('#country').val();
        let state = $(this).val();
        if (state) {
            $.ajax({
                url: '/cities',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({country: country, state: state}),
                success: function(data) {
                    $('#city').empty().append('<option value="">Select City</option>');
                    $.each(data, function(index, value) {
                        $('#city').append('<option value="' + value + '">' + value + '</option>');
                    });
                    $('#city').prop('disabled', false);
                }
            });
        } else {
            $('#city').empty().append('<option value="">Select City</option>').prop('disabled', true);
        }
    });

    $('#location-form').submit(function(event) {
        event.preventDefault();  // Prevent default form submission
        
        // Collect form data
        let formData = {
            country: $('#country').val(),
            state: $('#state').val(),
            city: $('#city').val(),
            zip_code: $('#zip_code').val()
        };
        
        // Send AJAX request to get weather
        $.ajax({
            url: '/weather',
            type: 'POST',
            data: formData,
            success: function(response) {
                // Redirect to weather result page with latitude and longitude
                if (response.latitude && response.longitude) {
                    window.location.href = `/weather-result?latitude=${response.latitude}&longitude=${response.longitude}`;
                } else {
                    $('#forecast').html(`<p>${response.error}</p>`);
                }
            },
            error: function(error) {
                $('#forecast').html(`<p>Error: Could not retrieve weather data.</p>`);
            }
        });
    });
});