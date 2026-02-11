console.log("✅ app.js loaded");

const input = document.getElementById("projectInput");
const sendBtn = document.getElementById("sendBtn");

const ideaBox = document.getElementById("ideaBox");
const planBox = document.getElementById("planBox");
const optionsBox = document.getElementById("optionsBox");

sendBtn.addEventListener("click", startProject);

function startProject() {
    const projectGoal = input.value.trim();

    if (!projectGoal) {
        alert("Please enter a project idea");
        return;
    }

    console.log("📤 Sending project:", projectGoal);

    fetch("/project/start-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_goal: projectGoal })
    })
    .then(res => res.json())
    .then(data => {
        console.log("📥 Backend response:", data);

        renderIdea(data.idea);
        renderPlan(data.plan);
        renderOptions(data.options);
    })
    .catch(err => {
        console.error("❌ Error:", err);
    });
}

/* ----------------- RENDER FUNCTIONS ----------------- */

function renderIdea(idea) {
    ideaBox.innerHTML = `
        <h3>💡 IDEA</h3>
        <pre>${idea || "No idea generated"}</pre>
    `;
}

function renderPlan(plan) {
    planBox.innerHTML = `
        <h3>🧠 PLAN</h3>
        <pre>${plan || "No plan available"}</pre>
    `;
}

function renderOptions(options) {
    optionsBox.innerHTML = `<h3>⚙️ OPTIONS</h3>`;

    if (!options || options.length === 0) {
        optionsBox.innerHTML += `<p>No options available</p>`;
        return;
    }

    options.forEach(option => {
        const btn = document.createElement("button");
        btn.textContent = option;
        btn.style.marginBottom = "8px";

        // 🔥 ATTACH CLICK HANDLER
        btn.onclick = () => handleOptionClick(option);

        optionsBox.appendChild(btn);
    });
}

/* ----------------- OPTION HANDLER ----------------- */

function handleOptionClick(option) {
    console.log("🟢 Option clicked:", option);

    fetch("/project/continue-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: option })
    })
    .then(res => res.json())
    .then(data => {
        console.log("📥 Continue response:", data);

        if (data.idea) renderIdea(data.idea);
        if (data.plan) renderPlan(data.plan);
    })
    .catch(err => {
        console.error("❌ Option error:", err);
    });
}
