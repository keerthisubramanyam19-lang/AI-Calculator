const expressionInput =
    document.getElementById("expression");

const calculatorForm =
    document.getElementById("calculatorForm");

const calculatorResult =
    document.getElementById("calculatorResult");

const showSteps =
    document.getElementById("showSteps");

const stepsPanel =
    document.getElementById("stepsPanel");

const micButton =
    document.getElementById("micButton");

const voiceText =
    document.getElementById("voiceText");

const aiButton =
    document.getElementById("aiButton");

const aiChat =
    document.getElementById("aiChat");

const closeChat =
    document.getElementById("closeChat");

const chatForm =
    document.getElementById("chatForm");

const chatInput =
    document.getElementById("chatInput");

const chatMessages =
    document.getElementById("chatMessages");

const historyList =
    document.getElementById("historyList");

const clearHistoryButton =
    document.getElementById("clearHistory");


let calculationHistory = [];

let aiHistory = [];


function addValue(value) {

    expressionInput.value += value;

    expressionInput.focus();

}


function clearDisplay() {

    expressionInput.value = "";

    calculatorResult.textContent = "";

    stepsPanel.innerHTML = "";

}


calculatorForm.addEventListener(
    "submit",
    function() {

        const expression =
            expressionInput.value.trim();

        if (!expression) {
            return;
        }

        calculationHistory.unshift({
            expression: expression
        });

        calculationHistory =
            calculationHistory.slice(0, 20);

        displayHistory();

    }
);


function displayHistory() {

    historyList.innerHTML = "";

    calculationHistory.forEach(
        function(item) {

            const div =
                document.createElement("div");

            div.className =
                "history-item";

            div.textContent =
                item.expression;

            div.addEventListener(
                "click",
                function() {

                    expressionInput.value =
                        item.expression;

                }
            );

            historyList.appendChild(div);

        }
    );

}


clearHistoryButton.addEventListener(
    "click",
    function() {

        calculationHistory = [];

        displayHistory();

    }
);


showSteps.addEventListener(
    "click",
    async function() {

        const expression =
            expressionInput.value.trim();

        if (!expression) {

            stepsPanel.innerHTML =
                '<div class="steps-error">Please enter a calculation first.</div>';

            return;

        }

        stepsPanel.innerHTML =
            '<div class="steps-loading">Calculating...</div>';

        try {

            const response =
                await fetch(
                    "/explain",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            expression:
                                expression
                        })
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                stepsPanel.innerHTML =
                    `<div class="steps-error">${data.error}</div>`;

                return;

            }

            displaySteps(data);

        } catch {

            stepsPanel.innerHTML =
                '<div class="steps-error">Unable to load explanation.</div>';

        }

    }
);


function displaySteps(data) {

    let html = "";

    html += `
        <div class="steps-result">
            ${data.expression} = ${data.result}
        </div>
    `;

    if (data.steps) {

        html += `
            <div class="steps-list">
        `;

        data.steps.forEach(
            function(step, index) {

                html += `
                    <div class="step">
                        <span>${index + 1}</span>
                        <p>${step}</p>
                    </div>
                `;

            }
        );

        html += `
            </div>
        `;

    }

    if (
        data.type === "sin" ||
        data.type === "cos" ||
        data.type === "tan"
    ) {

        html += createUnitCircle(data);

    }

    stepsPanel.innerHTML = html;

    if (
        data.type === "sin" ||
        data.type === "cos" ||
        data.type === "tan"
    ) {

        const section =
            stepsPanel.querySelector(
                ".unit-circle-section"
            );

        if (section) {

            animateUnitCircle(
                section,
                data.angle
            );

        }

    }

}


function createUnitCircle(data) {

    return `
        <div class="unit-circle-section">

            <div class="unit-circle-title">
                Visual Explanation
            </div>

            <div class="unit-circle-visual">

                <svg
                    class="unit-circle-svg"
                    viewBox="0 0 360 360"
                >

                    <line
                        x1="30"
                        y1="180"
                        x2="330"
                        y2="180"
                        class="circle-axis"
                    />

                    <line
                        x1="180"
                        y1="30"
                        x2="180"
                        y2="330"
                        class="circle-axis"
                    />

                    <circle
                        cx="180"
                        cy="180"
                        r="120"
                        class="unit-circle"
                    />

                    <line
                        id="animatedRadius"
                        x1="180"
                        y1="180"
                        x2="180"
                        y2="180"
                        class="animated-radius"
                    />

                    <line
                        id="animatedYLine"
                        x1="180"
                        y1="180"
                        x2="180"
                        y2="180"
                        class="y-line"
                    />

                    <path
                        id="angleArc"
                        class="angle-arc"
                    />

                    <circle
                        id="animatedPoint"
                        cx="180"
                        cy="180"
                        r="6"
                        class="animated-point"
                    />

                    <text
                        x="320"
                        y="172"
                        class="circle-label"
                    >
                        x
                    </text>

                    <text
                        x="188"
                        y="42"
                        class="circle-label"
                    >
                        y
                    </text>

                    <text
                        id="angleLabel"
                        x="190"
                        y="165"
                        class="angle-label"
                    ></text>

                    <text
                        id="animationStatus"
                        x="180"
                        y="345"
                        text-anchor="middle"
                        class="animation-status"
                    ></text>

                </svg>

            </div>

            <div class="unit-circle-info">

                <div>
                    <span>X-coordinate</span>
                    <strong id="circleX">0</strong>
                </div>

                <div>
                    <span>Y-coordinate</span>
                    <strong id="circleY">0</strong>
                </div>

                <div>
                    <span>Function</span>
                    <strong>${data.expression}</strong>
                </div>

            </div>

            <div class="visual-explanation">

                <div class="visual-function">
                    ${data.expression}
                </div>

                <div class="visual-message">
                    The point moves around the unit circle
                    until it reaches the required angle.
                </div>

            </div>

        </div>
    `;

}


function animateUnitCircle(
    section,
    targetAngle
) {

    const radius = 120;

    const centerX = 180;

    const centerY = 180;

    const point =
        section.querySelector(
            "#animatedPoint"
        );

    const radiusLine =
        section.querySelector(
            "#animatedRadius"
        );

    const yLine =
        section.querySelector(
            "#animatedYLine"
        );

    const angleLabel =
        section.querySelector(
            "#angleLabel"
        );

    const status =
        section.querySelector(
            "#animationStatus"
        );

    const circleX =
        section.querySelector(
            "#circleX"
        );

    const circleY =
        section.querySelector(
            "#circleY"
        );

    const angleArc =
        section.querySelector(
            "#angleArc"
        );


    const duration = 1800;

    const startTime =
        performance.now();


    function easeInOut(t) {

        return t < 0.5
            ? 2 * t * t
            : 1 - Math.pow(-2 * t + 2, 2) / 2;

    }


    function createArc(angle) {

        const radians =
            angle * Math.PI / 180;

        const startX =
            centerX + radius;

        const startY =
            centerY;

        const endX =
            centerX +
            radius *
            Math.cos(radians);

        const endY =
            centerY -
            radius *
            Math.sin(radians);

        const largeArc =
            Math.abs(angle) > 180
                ? 1
                : 0;

        const sweep =
            angle >= 0
                ? 0
                : 1;

        return `
            M ${startX} ${startY}
            A ${radius} ${radius}
            0 ${largeArc} ${sweep}
            ${endX} ${endY}
        `;

    }


    function animate(now) {

        const progress =
            Math.min(
                (now - startTime) / duration,
                1
            );

        const currentAngle =
            targetAngle *
            easeInOut(progress);

        const radians =
            currentAngle *
            Math.PI / 180;

        const x =
            Math.cos(radians);

        const y =
            Math.sin(radians);

        const px =
            centerX + radius * x;

        const py =
            centerY - radius * y;


        point.setAttribute(
            "cx",
            px
        );

        point.setAttribute(
            "cy",
            py
        );


        radiusLine.setAttribute(
            "x2",
            px
        );

        radiusLine.setAttribute(
            "y2",
            py
        );


        yLine.setAttribute(
            "x1",
            px
        );

        yLine.setAttribute(
            "y1",
            py
        );

        yLine.setAttribute(
            "x2",
            px
        );

        yLine.setAttribute(
            "y2",
            centerY
        );


        angleArc.setAttribute(
            "d",
            createArc(currentAngle)
        );


        angleLabel.textContent =
            `${currentAngle.toFixed(0)}°`;


        circleX.textContent =
            x.toFixed(3);

        circleY.textContent =
            y.toFixed(3);


        status.textContent =
            progress < 1
                ? "Moving to angle..."
                : "Angle reached";


        if (progress < 1) {

            requestAnimationFrame(
                animate
            );

        }

    }


    requestAnimationFrame(
        animate
    );

}


const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    const recognition =
        new SpeechRecognition();

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.lang = "en-IN";


    micButton.addEventListener(
        "click",
        function() {

            try {

                recognition.start();

                voiceText.textContent =
                    "Listening...";

                micButton.textContent =
                    "🔴";

            } catch {

                recognition.stop();

            }

        }
    );


    recognition.onresult =
        async function(event) {

            const spokenText =
                event.results[0][0]
                    .transcript
                    .trim();

            voiceText.textContent =
                spokenText;

            micButton.textContent =
                "⏳";

            try {

                const response =
                    await fetch(
                        "/voice",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                message:
                                    spokenText
                            })
                        }
                    );

                const data =
                    await response.json();


                if (
                    data.type ===
                    "calculation"
                ) {

                    expressionInput.value =
                        data.expression;

                    calculatorResult.textContent =
                        data.answer;

                    calculationHistory.unshift({
                        expression:
                            data.expression
                    });

                    calculationHistory =
                        calculationHistory.slice(
                            0,
                            20
                        );

                    displayHistory();

                    voiceText.textContent =
                        `${data.expression} = ${data.answer}`;

                    speakAnswer(
                        data.answer
                    );

                } else {

                    voiceText.textContent =
                        data.answer;

                    speakAnswer(
                        data.answer
                    );

                }

            } catch {

                voiceText.textContent =
                    "Unable to process voice";

            }

            micButton.textContent =
                "🎙️";

        };


    recognition.onerror =
        function() {

            micButton.textContent =
                "🎙️";

            voiceText.textContent =
                "Please try again";

        };


    recognition.onend =
        function() {

            micButton.textContent =
                "🎙️";

        };

} else {

    micButton.disabled = true;

    voiceText.textContent =
        "Voice not supported";

}


function speakAnswer(text) {

    if (
        !("speechSynthesis" in window)
    ) {
        return;
    }

    speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(
            text
        );

    speech.lang =
        "en-IN";

    speech.rate =
        0.95;

    speechSynthesis.speak(
        speech
    );

}


if (aiButton && aiChat) {

    aiButton.addEventListener(
        "click",
        function() {

            aiChat.classList.add(
                "active"
            );

            if (chatInput) {
                chatInput.focus();
            }

        }
    );

}


if (closeChat && aiChat) {

    closeChat.addEventListener(
        "click",
        function() {

            aiChat.classList.remove(
                "active"
            );

        }
    );

}


if (chatForm) {

    chatForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const message =
                chatInput.value.trim();

            if (!message) {
                return;
            }


            addChatMessage(
                message,
                "user-message"
            );


            aiHistory.push({
                role: "user",
                content: message
            });


            chatInput.value = "";


            const loading =
                addChatMessage(
                    "Thinking...",
                    "ai-message"
                );


            try {

                const response =
                    await fetch(
                        "/ai",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                message: message,
                                history:
                                    aiHistory
                            })
                        }
                    );


                const data =
                    await response.json();


                loading.remove();


                if (
                    data.type === "graph"
                ) {

                    const graph =
                        createTrigGraph(
                            data
                        );

                    chatMessages.appendChild(
                        graph
                    );

                } else {

                    addChatMessage(
                        data.answer ||
                        "Sorry, I couldn't process that request.",
                        "ai-message"
                    );

                }


                aiHistory.push({
                    role: "assistant",
                    content:
                        data.answer ||
                        JSON.stringify(data)
                });


            } catch {

                loading.remove();

                addChatMessage(
                    "Sorry, I couldn't process that request.",
                    "ai-message"
                );

            }

        }
    );

}


function addChatMessage(
    message,
    className
) {

    const div =
        document.createElement("div");

    div.className =
        className;

    div.textContent =
        message;

    chatMessages.appendChild(
        div
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

    return div;

}


function createTrigGraph(data) {

    const container =
        document.createElement("div");

    container.className =
        "ai-graph-container";


    const title =
        document.createElement("div");

    title.className =
        "graph-title";

    title.textContent =
        `${data.function} graph`;

    container.appendChild(
        title
    );


    const canvas =
        document.createElement("canvas");

    canvas.width = 600;

    canvas.height = 320;

    canvas.className =
        "trig-graph";

    container.appendChild(
        canvas
    );


    const ctx =
        canvas.getContext("2d");

    const width =
        canvas.width;

    const height =
        canvas.height;


    ctx.clearRect(
        0,
        0,
        width,
        height
    );


    ctx.strokeStyle =
        "#555";

    ctx.lineWidth = 1;


    ctx.beginPath();

    ctx.moveTo(
        0,
        height / 2
    );

    ctx.lineTo(
        width,
        height / 2
    );

    ctx.stroke();


    ctx.beginPath();

    ctx.moveTo(
        width / 2,
        0
    );

    ctx.lineTo(
        width / 2,
        height
    );

    ctx.stroke();


    ctx.strokeStyle =
        "#ffffff";

    ctx.lineWidth = 2;

    ctx.beginPath();


    for (
        let pixel = 0;
        pixel <= width;
        pixel++
    ) {

        const angle =
            (
                pixel / width
            ) *
            720 -
            360;

        const radians =
            angle *
            Math.PI /
            180;

        let value;


        if (
            data.function === "sin"
        ) {

            value =
                Math.sin(radians);

        } else if (
            data.function === "cos"
        ) {

            value =
                Math.cos(radians);

        } else {

            value =
                Math.tan(radians);

        }


        if (
            Math.abs(value) > 5
        ) {

            ctx.moveTo(
                pixel,
                height / 2
            );

            continue;

        }


        const y =
            height / 2 -
            value * 70;


        if (pixel === 0) {

            ctx.moveTo(
                pixel,
                y
            );

        } else {

            ctx.lineTo(
                pixel,
                y
            );

        }

    }


    ctx.stroke();


    if (
        data.angle !== null &&
        data.angle !== undefined
    ) {

        const angle =
            Number(data.angle);

        const x =
            (
                angle + 360
            ) /
            720 *
            width;

        const radians =
            angle *
            Math.PI /
            180;

        let value;


        if (
            data.function === "sin"
        ) {

            value =
                Math.sin(radians);

        } else if (
            data.function === "cos"
        ) {

            value =
                Math.cos(radians);

        } else {

            value =
                Math.tan(radians);

        }


        if (
            Math.abs(value) <= 5
        ) {

            const y =
                height / 2 -
                value * 70;

            ctx.fillStyle =
                "#ffffff";

            ctx.beginPath();

            ctx.arc(
                x,
                y,
                5,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }

    }


    return container;

}