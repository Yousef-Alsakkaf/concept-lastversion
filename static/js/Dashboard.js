document.addEventListener("DOMContentLoaded", () => {
    // Random Statistics
    document.getElementById("total-users").textContent = Math.floor(Math.random() * 1000) + 100;
    document.getElementById("monthly-revenue").textContent = `$${(Math.random() * 10000).toFixed(2)}`;
    document.getElementById("active-agents").textContent = Math.floor(Math.random() * 100) + 10;
    document.getElementById("support-tickets").textContent = Math.floor(Math.random() * 500) + 50;

    // Revenue Chart
    const revenueCtx = document.getElementById("revenueChart").getContext("2d");
    new Chart(revenueCtx, {
        type: "line",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
            datasets: [
                {
                    label: "Monthly Revenue",
                    data: Array.from({ length: 7 }, () => Math.random() * 10000),
                    backgroundColor: "rgba(103, 58, 183, 0.2)",
                    borderColor: "rgba(103, 58, 183, 1)",
                    borderWidth: 2,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                },
            },
        },
    });

    // User Growth Chart
    const userGrowthCtx = document.getElementById("userGrowthChart").getContext("2d");
    new Chart(userGrowthCtx, {
        type: "bar",
        data: {
            labels: ["2018", "2019", "2020", "2021", "2022", "2023"],
            datasets: [
                {
                    label: "User Growth",
                    data: Array.from({ length: 6 }, () => Math.random() * 500),
                    backgroundColor: "rgba(103, 58, 183, 0.5)",
                    borderColor: "rgba(103, 58, 183, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                },
            },
        },
    });
});
