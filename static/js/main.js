/* ===================== 
   AOS INITIALIZATION
===================== */
AOS.init({
  duration: 1000
});

/* =====================
   ACTIVE NAV TAB
===================== */
const page = location.pathname.split("/").pop() || "templates/index.html";
document.querySelectorAll(".menu a").forEach(link => {
  if (link.getAttribute("href") === page) {
    link.classList.add("active-tab");
  }
});

/* =====================
   CURSOR GLOW
===================== */
const cursor = document.querySelector(".cursor-glow");

if (cursor) {
  window.addEventListener("mousemove", e => {
    cursor.style.left = e.clientX + "px";
    cursor.style.top = e.clientY + "px";
  });
}

/* =====================
   MOBILE MENU TOGGLE
===================== */
const toggle = document.getElementById("menuToggle");
const menu = document.getElementById("menu");

if (toggle && menu) {

  // Open / close menu
  toggle.addEventListener("click", () => {
    menu.classList.toggle("show");
  });

  // Close menu when a link is clicked (IMPORTANT)
  document.querySelectorAll(".menu a").forEach(link => {
    link.addEventListener("click", () => {
      menu.classList.remove("show");
    });
  });
}

/* =====================
   CHARTS (HOME PAGE ONLY)
===================== */
const bar = document.getElementById("barChart");
const line = document.getElementById("lineChart");

if (bar && line && typeof Chart !== "undefined") {

  new Chart(bar, {
    type: "bar",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [{
        label: "Projects",
        data: [10, 20, 35, 45, 60, 80],
        backgroundColor: "#38bdf8"
      }]
    },
    options: {
      animation: { duration: 2000 },
      responsive: true
    }
  });

  new Chart(line, {
    type: "line",
    data: {
      labels: ["2019", "2020", "2021", "2022", "2023", "2024"],
      datasets: [{
        label: "Growth %",
        data: [20, 35, 45, 60, 75, 92],
        borderColor: "#22c55e",
        backgroundColor: "rgba(34,197,94,0.3)",
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      animation: { duration: 2200 },
      responsive: true
    }
  });

}

/* =====================
   CONTACT FORM AJAX
===================== */
const contactForm = document.getElementById("contactForm");
const successBox = document.getElementById("formSuccess");

if (contactForm) {
  contactForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // stop page reload

    const formData = new FormData(contactForm);

    try {
      const response = await fetch("/submit-contact", {
        method: "POST",
        body: formData
      });

      if (response.ok) {
        successBox.style.display = "block";
        contactForm.reset();

        // Auto-hide after 5 seconds (optional)
        setTimeout(() => {
          successBox.style.display = "none";
        }, 5000);
      }
    } catch (error) {
      alert("Something went wrong. Please try again.");
    }
  });
}
