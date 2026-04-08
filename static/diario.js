document.addEventListener("DOMContentLoaded", () => {
    const pages = Array.from(document.querySelectorAll(".diary-page"));
    if (pages.length === 0) return;

    let current = 0;

    function showPage(index) {
        pages.forEach((p, i) => {
            p.style.display = (i === index) ? "block" : "none";
        });
    }

    showPage(current);

    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    prevBtn.addEventListener("click", () => {
        if (current > 0) {
            current -= 1;
            showPage(current);
        }
    });

    nextBtn.addEventListener("click", () => {
        if (current < pages.length - 1) {
            current += 1;
            showPage(current);
        }
    });
});
// Gestione della croce per aggiungere una nuova pagina
const addButton = document.getElementById("addButton");
const fileInput = document.getElementById("fileInput");
const addForm = document.getElementById("addForm");

if (addButton) {
    addButton.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener("change", () => {
        addForm.submit();
    });
}
// Gestione didascalie
document.querySelectorAll(".caption-box").forEach(box => {
    const text = box.querySelector(".caption-text");
    const editBtn = box.querySelector(".edit-caption-btn");
    const form = box.querySelector(".caption-form");
    const input = box.querySelector(".caption-input");

    editBtn.addEventListener("click", () => {
        text.style.display = "none";
        editBtn.style.display = "none";
        form.style.display = "block";
        input.focus();
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form)
        });

        if (response.ok) {
            text.textContent = input.value;
            text.style.display = "block";
            editBtn.style.display = "inline-block";
            form.style.display = "none";
        }
    });
});
// Mostra la modalità modifica
document.querySelectorAll(".edit-caption-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const box = btn.closest(".caption-box");

        box.querySelector(".caption-text").style.display = "none";
        box.querySelector(".caption-form").style.display = "block";
        box.querySelector(".delete-form").style.display = "block";

        btn.style.display = "none";
    });
});

// Overlay elimina
document.querySelectorAll(".open-delete").forEach(btn => {
    btn.addEventListener("click", function () {
        const form = btn.closest("form");
        const action = form.getAttribute("action");

        document.getElementById("confirmDeleteForm").setAttribute("action", action);
        document.getElementById("deleteOverlay").style.display = "flex";
    });
});

// Chiudi overlay
document.getElementById("cancelDelete").addEventListener("click", function () {
    document.getElementById("deleteOverlay").style.display = "none";
});
