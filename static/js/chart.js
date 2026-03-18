document.addEventListener("DOMContentLoaded", async () => {
  const canvas = document.getElementById("pendapatanChart");
  const graphExpense = document.getElementById("pengeluaranChart");
  const chartPie = document.getElementById("chart-pie");

  // INCOME CHART
  if (canvas) {
    try {
      const res = await fetch("/api/income-monthly");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      const chartLabels = data.map(item => item.bulan);
      const chartValues = data.map(item => Number(item.total) || 0);

      new Chart(canvas, {
        type: "line",
        data: {
          labels: chartLabels,
          datasets: [{
            label: "Expense 5 Bulan Terakhir",
            data: chartValues,
            borderColor: "#4cc9f0", 
            backgroundColor: "rgba(76, 201, 240, 0.1)",
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: "#4cc9f0",
            pointBorderColor: "#fff",
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: "#cbd5e1" // warna text legend biar soft
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: "#94a3b8"
              },
              grid: {
                color: "rgba(255,255,255,0.05)"
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: "#94a3b8"
              },
              grid: {
                color: "rgba(255,255,255,0.05)"
              }
            }
          }
        }
      });
    } catch (err) {
      console.error("Gagal ambil data income:", err);
    }
  }

  // EXPENSE CHART
  if (graphExpense) {
    try {
      const res = await fetch("/api/expense-monthly");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      const chartLabels = data.map(item => item.bulan);
      const chartValues = data.map(item => Number(item.total) || 0);

      new Chart(graphExpense, {
        type: "line",
        data: {
          labels: chartLabels,
          datasets: [{
            label: "Expense 5 Bulan Terakhir",
            data: chartValues,
            borderColor: "#4cc9f0", // warna neon biru
            backgroundColor: "rgba(76, 201, 240, 0.1)",
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: "#4cc9f0",
            pointBorderColor: "#fff",
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: "#cbd5e1" // warna text legend biar soft
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: "#94a3b8"
              },
              grid: {
                color: "rgba(255,255,255,0.05)"
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: "#94a3b8"
              },
              grid: {
                color: "rgba(255,255,255,0.05)"
              }
            }
          }
        }
      });
    } catch (err) {
      console.error("Gagal ambil data expense:", err);
    }
  }

    // PIE / DOUGHNUT CHART
    if (chartPie) {
      try {
        const res = await fetch("/api/type-cost");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();
        console.log("pie data:", data);

        const categoryType = data.map(item => item.category || "Tanpa Kategori");
        const amountMonth = data.map(item => Number(item.total) || 0);

        new Chart(chartPie, {
          type: "doughnut",
          data: {
            labels: categoryType,
            datasets: [{
              label: "Expense Bulan Ini",
              data: amountMonth,
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });

      } catch (err) {
        console.error("Gagal ambil data pie expense:", err);
      }
    }


});