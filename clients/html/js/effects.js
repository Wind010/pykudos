function cheer() {
    const defaults = {
        spread: 365,
        ticks: 101,
        gravity: 0,
        decay: 0.93,
        startVelocity: 31,
    };

    function shoot() {
        confetti({
            ...defaults,
            particleCount: 32,
            scalar: 1.2,
            shapes: ["circle", "square"],
            colors: ["#a864fd", "#29cdff", "#78ff44", "#ff718d", "#fdff6a"],
        });

        confetti({
            ...defaults,
            particleCount: 60,
            scalar: 5,
            shapes: ["emoji", "image"],
            shapeOptions: {
                emoji: {
                    value: ["🚀", "💖", "⭐", "🖖"],
                },
                image: [{
                    src: "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",
                    width: 32,
                    height: 32,
                  }
                ]
            },
        });
    }

    setTimeout(shoot, 0);
    setTimeout(shoot, 100);
    setTimeout(shoot, 200);
}