const API_URL = "";

const myJobs = JSON.parse(
    localStorage.getItem("myJobs") || "[]"
);

let pollingInterval = null;


const PIPELINE_STEPS = [
    { key: "queued",          icon: "⏳", label: "Queued" },
    { key: "extracting_pdf",  icon: "📄", label: "Extract PDF" },
    { key: "summarizing",     icon: "🤖", label: "AI Summary" },
    { key: "generating_docx", icon: "📝", label: "Create DOCX" },
    { key: "completed",       icon: "✓", label: "Done" }
];


function getStepIndex(status) {
    const idx = PIPELINE_STEPS.findIndex(
        s => s.key === status
    );
    return idx === -1 ? 0 : idx;
}


function getProgressPercent(status) {
    const map = {
        queued: 5,
        extracting_pdf: 25,
        summarizing: 55,
        generating_docx: 80,
        completed: 100,
        failed: 0
    };
    return map[status] ?? 0;
}


function buildStepper(status) {
    const currentIdx = getStepIndex(status);
    const isFailed = status === "failed";

    const isCompleted = status === "completed";

    const steps = PIPELINE_STEPS.map((step, i) => {
        let state = "upcoming";
        if (isFailed) {
            state = i <= currentIdx ? "failed" : "upcoming";
        } else if (isCompleted || i < currentIdx) {
            state = "done";
        } else if (i === currentIdx) {
            state = "active";
        }

        return `
            <div class="step ${state}">
                <div class="step-dot">
                    ${state === "done" ? "✓" : step.icon}
                </div>
                <div class="step-label">
                    ${step.label}
                </div>
            </div>
        `;
    }).join("");

    const percent = getProgressPercent(status);

    return `
        <div class="stepper">
            <div class="stepper-track">
                <div
                    class="stepper-fill ${isFailed ? 'stepper-fill-failed' : ''}"
                    style="width: ${percent}%"
                ></div>
            </div>
            <div class="stepper-steps">
                ${steps}
            </div>
        </div>
    `;
}


function getDisplayStatus(status) {
    const statusMap = {
        queued: "Queued",
        extracting_pdf: "Extracting PDF",
        summarizing: "Generating AI Summary",
        generating_docx: "Creating Word File",
        completed: "Completed",
        failed: "Failed"
    };
    return statusMap[status] || status;
}


function showToast(message) {
    const existing = document.querySelector(".toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add("toast-visible");
    });

    setTimeout(() => {
        toast.classList.remove("toast-visible");
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}


async function createJob() {
    const input = document.getElementById("fileInput");
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(
            `${API_URL}/jobs`,
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            const error = await response.json().catch(
                () => ({ detail: "Upload failed" })
            );
            showToast(
                `✗ ${error.detail || "Upload failed"}`
            );
            return;
        }

        const data = await response.json();
        myJobs.push(data.job_id);
        localStorage.setItem(
            "myJobs",
            JSON.stringify(myJobs)
        );
        input.value = "";

        showToast(
            `✓ "${file.name}" uploaded — processing started!`
        );
    } catch (e) {
        showToast(
            "✗ Connection error — is the server running?"
        );
    }
}


async function fetchJobs() {
    try {
        const response = await fetch(
            `${API_URL}/jobs`
        );
        const jobs = await response.json();

        const filteredJobs = jobs.filter(
            job => myJobs.includes(job.id)
        );

        renderJobs(filteredJobs);
    } catch (e) {
        console.error("Failed to fetch jobs:", e);
    }
}


function renderJobs(jobs) {
    const container = document.getElementById(
        "jobsContainer"
    );

    container.innerHTML = "";

    if (jobs.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                No jobs yet — upload a PDF to get started
            </div>
        `;
        return;
    }

    jobs.forEach(job => {
        const card = document.createElement("div");
        card.className = "job-card";

        const isProcessing = [
            "extracting_pdf",
            "summarizing",
            "generating_docx"
        ].includes(job.status);

        const showStepper =
            job.status !== "queued" || isProcessing;

        card.innerHTML = `
            <div class="job-header">
                <div>
                    <div class="filename">
                        ${job.filename}
                    </div>
                    <div class="job-id">
                        ${job.id}
                    </div>
                </div>

                <div class="status-pill ${job.status}">
                    ${isProcessing ? '<span class="pulse-dot"></span>' : ''}
                    ${getDisplayStatus(job.status)}
                </div>
            </div>

            ${buildStepper(job.status)}

            ${
                job.status === "completed"
                ? `
                <a
                    href="${API_URL}/jobs/${job.id}/download"
                    class="download-btn"
                >
                    ⬇ Download Summary
                </a>
                `
                : ""
            }

            ${
                job.status === "failed"
                ? `
                <div class="error-msg">
                    Processing failed. Please try uploading again.
                </div>
                `
                : ""
            }
        `;

        container.appendChild(card);
    });
}


function openModal() {
    document
        .getElementById("statusModal")
        .classList.remove("hidden");

    fetchJobs();

    if (!pollingInterval) {
        pollingInterval = setInterval(
            fetchJobs, 2000
        );
    }
}


function closeModal() {
    document
        .getElementById("statusModal")
        .classList.add("hidden");

    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}
