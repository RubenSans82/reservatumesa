var bookings = JSON.parse(document.getElementById('bookings-data').textContent);
var people = document.getElementById('people');
var date = document.getElementById('date');

people.addEventListener('change', checkTime);
date.addEventListener('change', checkTime);

function checkTime() {
    var date_value = date.value;
    var people_value = people.value;
    var time = document.getElementById('time');
    time.innerHTML = ''; // Clear previous options
    var booking_time = new Date(date_value + 'T13:00:00');
    var booking_end = new Date(date_value + 'T15:00:01');
    while (booking_time < booking_end) {
        var available = checkAvailability(booking_time, people_value);
        if (available) {
            time.innerHTML += '<option value="' + booking_time.toTimeString().slice(0, 5) + '">' + booking_time.toTimeString().slice(0, 5) + '</option>';
        }
        booking_time.setMinutes(booking_time.getMinutes() + 30); // Incrementar el tiempo en 30 minutos
    }
}

function checkAvailability(booking_time, people) {
    var available = true;
    var booking_time_minus_90 = new Date(booking_time.getTime() - 90 * 60000); // Restar 90 minutos
    var booking_time_plus_90 = new Date(booking_time.getTime() + 90 * 60000); // Añadir 90 minutos
    var people_before = 0;
    var people_after = 0;
    for (var i = 0; i < bookings.length; i++) {
        var booking_start = new Date(bookings[i].date + 'T' + bookings[i].time);
        if (booking_start <= booking_time && booking_start >= booking_time_minus_90) {
            people_before += bookings[i].diners;
        }
        if (booking_start >= booking_time && booking_start <= booking_time_plus_90) {
            people_after += bookings[i].diners;
        }
    }
    if ((people_before + parseInt(people) > 30) || (people_after + parseInt(people) > 30)) {
        available = false;
    }
    return available;
}

