let startX, thumbPosition, maxThumbPosition;

const initSlide = () => {
    const slideButtons = document.querySelectorAll(
        ".programmer-slider-wrapper .slide-button"
    );
    const imageList = document.querySelector(".programmer-slider-wrapper .image-list");
    const sliderScrollBar = document.querySelector(
        ".slider-container .slider-scrollBar"
    );
    const scrollBarThumb = sliderScrollBar.querySelector(".scrollBar-thumb");
    const maxScrollLeft = imageList.scrollWidth - imageList.clientWidth;

    const handleMouseMove = (e) => {
        const deltaX = e.clientX - startX;
        const newThumbPosition = thumbPosition + deltaX;

        const boundedPosition = Math.max(
            0,
            Math.min(maxThumbPosition, newThumbPosition)
        );

        const scrollPosition =
            (boundedPosition / maxThumbPosition) * maxScrollLeft;

        scrollBarThumb.style.position = "absolute";
        scrollBarThumb.style.left = `${boundedPosition}px`;
        imageList.scrollLeft = scrollPosition;
    };

    const handleMouseUp = () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
    };

    scrollBarThumb.addEventListener("mousedown", (e) => {
        startX = e.clientX;
        thumbPosition = scrollBarThumb.offsetLeft;
        maxThumbPosition =
            sliderScrollBar.getBoundingClientRect().width -
            scrollBarThumb.offsetWidth;

        document.addEventListener("mousemove", handleMouseMove);
        document.addEventListener("mouseup", handleMouseUp);
    });

    // Slide images according to the slide button clicks
    slideButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const direction = button.id === "prev-slide" ? -1 : 1;
            const scrollAmount = imageList.clientWidth * direction;
            imageList.scrollBy({
                left: scrollAmount,
                behavior: "smooth",
            });
        });
    });

    const handleSlideButton = () => {
        slideButtons[0].style.display =
            imageList.scrollLeft <= 0 ? "none" : "block";
        slideButtons[1].style.display =
            imageList.scrollLeft >= maxScrollLeft ? "none" : "block";
    };

    const updateScrollThumbPosition = () => {
        const scrollPosition = imageList.scrollLeft;
        const thumbPosition =
            (scrollPosition / maxScrollLeft) *
            (sliderScrollBar.clientWidth - scrollBarThumb.offsetWidth);
        scrollBarThumb.style.position = "absolute";
        scrollBarThumb.style.left = `${thumbPosition}px`;
    };

    imageList.addEventListener("scroll", () => {
        handleSlideButton();
        updateScrollThumbPosition();
    });
};

window.addEventListener("load", initSlide);
