document.addEventListener("DOMContentLoaded", function () {

    const city = document.getElementById("id_city");
    const locality = document.getElementById("id_locality");
    const area = document.getElementById("id_area");
    const postal = document.getElementById("id_postal_code");

    if (!city || !locality || !area) {
        return;
    }

    function reset(select) {

        if (!select) return;

        select.innerHTML = '<option value="">---------</option>';
        select.disabled = true;

    }

    async function loadLocalities(cityId, selected = "") {

        reset(locality);
        reset(area);
        reset(postal);

        if (!cityId) return;

        const response = await fetch(
            "/admin/ajax/localities/?city=" + cityId
        );

        const rows = await response.json();

        rows.forEach(function (row) {

            locality.appendChild(
                new Option(
                    row.name,
                    row.id,
                    row.id == selected,
                    row.id == selected
                )
            );

        });

        locality.disabled = false;

        if (selected) {
            loadAreas(selected, area.value);
        }

    }

    async function loadAreas(localityId, selected = "") {

        reset(area);
        reset(postal);

        if (!localityId) return;

        const response = await fetch(
            "/admin/ajax/areas/?locality=" + localityId
        );

        const rows = await response.json();

        rows.forEach(function (row) {

            area.appendChild(
                new Option(
                    row.name,
                    row.id,
                    row.id == selected,
                    row.id == selected
                )
            );

        });

        area.disabled = false;

    }

    city.addEventListener("change", function () {

        loadLocalities(this.value);

    });

    locality.addEventListener("change", function () {

        loadAreas(this.value);

    });

    if (city.value) {

        loadLocalities(
            city.value,
            locality.value
        );

    } else {

        reset(locality);
        reset(area);
        reset(postal);

    }

});