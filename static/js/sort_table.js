function sortTable(n) {
    var table, sortable_rows, switching, i, x, y, shouldSwitch, dir, switch_count = 0;
    table = document.getElementById("verifications_list");
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        sortable_rows = table.getElementsByClassName("sortable-row");
        rows = table.rows
        /*Loop through all table sortable_rows (except the
        first, which contains table headers):*/
        for (i = 0; i < (sortable_rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/

            x = sortable_rows[i].getElementsByTagName("td")[n].getElementsByTagName("input")[0];
            y = sortable_rows[i + 1].getElementsByTagName("td")[n].getElementsByTagName("input")[0];
            /*check if the two sortable_rows should switch place,
            based on the direction, asc or desc:*/

            if (dir == "asc") {
                if (x.value.replace(' ', '').toLowerCase() > y.value.replace(' ', '').toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.value.replace(' ', '').toLowerCase() < y.value.replace(' ', '').toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
            //console.log(x.value.replace(' ', '').toLowerCase() + " " + y.value.replace(' ', '').toLowerCase())

        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            sortable_rows[i].parentNode.insertBefore(sortable_rows[i + 1], sortable_rows[i]);

            switching = true;
            //Each time a switch is done, increase this count by 1:
            switch_count++;
        } else {
            /*If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again.*/
            if (switch_count == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

function sort_floating_table(n) {
    var table, sortable_rows, switching, i, x, y, shouldSwitch, dir, switch_count = 0;
    table = document.getElementById("verifications_list");
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        sortable_rows = table.getElementsByClassName("sortable-row");
        rows = table.rows
        for (i = 0; i < (sortable_rows.length - 1); i++) {
            shouldSwitch = false;
            x = sortable_rows[i].getElementsByTagName("td")[n].getElementsByTagName("input")[0];
            y = sortable_rows[i + 1].getElementsByTagName("td")[n].getElementsByTagName("input")[0];
            x_to_sort = parseFloat(x.value.replace(' ', '').replace(' ', ''))
            y_to_sort = parseFloat(y.value.replace(' ', '').replace(' ', ''))

            if (dir == "asc") {
                if (x_to_sort > y_to_sort) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x_to_sort < y_to_sort) {
                    shouldSwitch = true;
                    break;
                }
            }
            if (sortable_rows[i].getElementsByTagName('input')[0].value == '47') {

            }

        }
        if (shouldSwitch) {
            sortable_rows[i].parentNode.insertBefore(sortable_rows[i + 1], sortable_rows[i]);

            switching = true;
            switch_count++;
        } else {
            if (switch_count == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}