

document.querySelectorAll(".walkthrough .item").forEach(function (item) {
    item.addEventListener("click", function (e) {
        let wt = item.closest(".walkthrough")
        let img = wt.querySelector(`.image-${item.dataset.item}`)
        if (img) {
            wt.querySelectorAll(".image").forEach(function (it) {
                it.classList.remove("active");
            })
            img.classList.add("active");
        }

        wt.querySelectorAll(".item").forEach(function (it) {
            it.classList.remove("active");
        })
        item.classList.add("active")
    })
})





